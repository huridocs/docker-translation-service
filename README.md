# Results

We are using the Helsinki-NLP/opus-100 (https://huggingface.co/datasets/Helsinki-NLP/opus-100) test set in Arabic, English, Spanish, French and Russian. The results are as follows:


| Model     | Prompt   | Arabic-English | English-Spanish | English-French | English-Russian |
|-----------|----------|----------------|-----------------|----------------|-----------------|
| llama3-8b | Prompt 1 | 19.4           | 29.38           | 27.03          | 15.73           |
| aya-8b    | Prompt 1 | 27.75          | 30.22           | 28.65          | 19.6            |
| aya-8b    | Prompt 2 | 27.73          | -               | -              | 20              |

(The scores have been calculated with fast-bleu https://pypi.org/project/fast-bleu/)

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
