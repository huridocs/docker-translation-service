# Results

We are using the Helsinki-NLP/opus-100 (https://huggingface.co/datasets/Helsinki-NLP/opus-100) test set in Arabic, English, Spanish, French and Russian. The results are as follows:

Performance 2000 samples

| Model      | Prompt   | Arabic-English | English-Spanish | English-French | English-Russian |
|------------|----------|----------------|-----------------|----------------|-----------------|
| DeepL      |          | 38.00          | -               | 35.73          | 26.94           |
| aya-35b    | Prompt 2 | 31.89          | -               | 32.57          | 22.91           |
| aya-8b     | Prompt 2 | 27.73          | -               | -              | 20              |
| aya-8b     | Prompt 1 | 27.75          | 30.22           | 28.65          | 19.6            |
| llama3-8b  | Prompt 1 | 19.4           | 29.38           | 27.03          | 15.73           |
| gemma2:27b | Prompt 2 | -              | -               | 21.58          | bad             |
| mixtral    | Prompt 2 | no ar          | -               | 18.15          | no rus          |
| llama3.1   | Prompt 2 | -              | 28.77           | 26.28          | -               |



Performance 100 samples

| Model        | Prompt   | Arabic-English | English-Spanish | English-French | English-Russian |
|--------------|----------|----------------|-----------------|----------------|-----------------|
| DeepL        |          | 33.11          | -               | 36.05          | 24.64           |
| aya-35b      | Prompt 2 | 30.75          | -               | 31.48          | 20.06           |
| glm4:9b      | Prompt 2 | 19.62          | -               | 30.21          | 16.12           |
| glm-BF16-64  | Prompt 2 | 18.75          | -               | 28.84          | 17.20           |
| glm-BF16-128 | Prompt 2 | 20.05          | -               | 30.09          | 17.82           |
| llama3.1     | Prompt 2 | 10.52          | 25.37           | 27.53          | 14.04           |








(The scores have been calculated with fast-bleu https://pypi.org/project/fast-bleu/ using the average score for bigrams and trigrams)

Prompts legend:


- Prompt 1: "Translate the below text to {translation_task.language_to}, "
             "keep the layout, do not skip any text, do not output anything else besides translation:"

- Prompt 2: """Please translate the following text into {translation_task.language_to}. Follow these guidelines:  
      1. Maintain the original layout and formatting.  
      2. Translate all text accurately without omitting any part of the content.  
      3. Preserve the tone and style of the original text.  
      4. Do not include any additional comments, notes, or explanations in the output; provide only the translated text.  

Here is the text to be translated:  
"""


Speed

| Model      | 1 sentence |
|------------|------------|
| DeepL      | 0.4s       |
| llama3-8b  | 0.86s      |
| aya-8b     | 0.925s     |
| aya-35b    | 3.3s       |
| gemma2:27b | 1.4s       |
| mixtral    | 2.5s       |
| glm4:9b    | 0.4s       |




# BLEU Score

| BLEU SCORE | INTERPRETATION                                       |
|------------|------------------------------------------------------|
| < 10       | Almost useless                                       |
| 10 - 19    | Hard to get the gist                                 |
| 20 - 29    | The gist is clear, but has significant errors        |
| 30 - 40    | Understandable to good translations                  |
| 40 - 50    | High quality translations                            |
| 50 - 60    | Very high quality, adequate, and fluent translations |
| > 60       | Quality often better than human                      |

# docker-translation-service

ollama serve
ollama run aya:35b

systemctl stop ollama
sudo service ollama stop

sudo kill -9 $(ps aux | grep 'ollama' | awk '{print $2}')
sudo kill -9 pid

root@debian:~# find /usr/share/ollama/.ollama/models/ -type f -exec chown ollama:ollama {} \;
root@debian:~# find /usr/share/ollama/.ollama/models/ -type d -exec chown ollama:ollama {} \;
root@debian:~# find /usr/share/ollama/.ollama/models/ -type f -exec chmod 644 {} \;
root@debian:~# find /usr/share/ollama/.ollama/models/ -type d -exec chmod 755 {} \;


https://hub.docker.com/r/ollama/ollama

docker run -d --gpus=all -v ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama

or

docker start ollama

docker exec -it ollama ollama run aya:35b
docker exec -it ollama-translations ollama pull aya:35b
docker exec -it ollama-translations ollama pull qwen:0.5b-text-v1.5-q2_K

curl http://localhost:11434/api/generate -d '{ "model": "aya:35b", "prompt": "What is water made of?" }'
curl http://localhost:7869/api/generate -d '{ "model": "tinyllama", "prompt": "What is water made of?" }'
curl http://localhost:8080/api/generate -d '{ "model": "glm-4-9b-chat", "prompt": "What is water made of?" }'


# Deployment

* For development purposes we can use dummy_extractor_services
  * If the language is "error" then the translation server returns an error
  * The other languages are returned with the text [translation for {language}] and the input text without been translated 
* Run it with "make docker" for having a docker container running mocking the translation service
* The deployment script is found in the "deployment repo" branch translations-service
* We have to set up a Google cloud server for this to run using GPUs 
  * or use a 24Gb ram server
* For deployment, we need the following environment variables: PROJECT_ID, INSTANCE_ID, ZONE, CREDENTIALS
* CREDENTIALS are found on the file /home/[user]/.config/gcloud/application_default_credentials.json
* The rest of variables are found on the Google Cloud Console

