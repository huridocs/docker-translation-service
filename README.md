# Results

We are using the Helsinki-NLP/opus-100 (https://huggingface.co/datasets/Helsinki-NLP/opus-100) test set in Arabic, English, Spanish, French and Russian. The results are as follows:

Performance

| Model     | Prompt   | Arabic-English | English-Spanish | English-French | English-Russian |
|-----------|----------|----------------|-----------------|----------------|-----------------|
| DeepL     |          | 38.00          | -               | 35.73          | 26.94           |
| llama3-8b | Prompt 1 | 19.4           | 29.38           | 27.03          | 15.73           |
| aya-8b    | Prompt 1 | 27.75          | 30.22           | 28.65          | 19.6            |
| aya-8b    | Prompt 2 | 27.73          | -               | -              | 20              |
| aya-35b   | Prompt 2 | 31.89          | -               | 32.57          | 22.91           |
| glm-BF16  | Prompt 2 | -              | -               | -              | -               |





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

| Model     | 1 sentence |
|-----------|------------|
| DeepL     | 0.4s       |
| llama3-8b | 0.86s      |
| aya-8b    | 0.925s     |
| aya-35b   | 3.3s       |




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
docker exec -it ollama-translations ollama pull tinyllama
docker exec -it ollama-translations ollama pull aya:35b

curl http://localhost:11434/api/generate -d '{ "model": "aya:35b", "prompt": "What is water made of?" }'
curl http://localhost:7869/api/generate -d '{ "model": "tinyllama", "prompt": "What is water made of?" }'
curl http://localhost:8080/api/generate -d '{ "model": "glm-4-9b-chat", "prompt": "What is water made of?" }'
