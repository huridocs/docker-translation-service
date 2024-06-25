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

curl http://localhost:11434/api/generate -d '{ "model": "aya:35b", "prompt": "What is water made of?" }'
