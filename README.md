# Results

We are using the Helsinki-NLP/opus-100 (https://huggingface.co/datasets/Helsinki-NLP/opus-100) test set in Arabic, English, Spanish, French and Russian. The results are as follows:

| Model  | promt        | Arabic | English    | Spanish | French   | Russian |
|--------|--------------|---------|------------|--------|----------|---------|
| llama3 | promt 1      | 0.950   | 0.939      | 0.968  | 0.981    | 0.981   |



promts legend:


1. promt 1: ""
2. promt 2: "


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

curl http://localhost:11434/api/generate -d '{ "model": "aya:35b", "prompt": "What is water made of?" }'
curl http://localhost:7869/api/generate -d '{ "model": "tinyllama", "prompt": "What is water made of?" }'
