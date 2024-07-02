install:
	. .venv/bin/activate; pip install -Ur requirements.txt

activate:
	. .venv/bin/activate

install_venv:
	python3 -m venv .venv
	. .venv/bin/activate; python -m pip install --upgrade pip
	. .venv/bin/activate; python -m pip install -r requirements.txt

formatter:
	. .venv/bin/activate; command black --line-length 125 .

check_format:
	. .venv/bin/activate; command black --line-length 125 . --check

remove_docker_containers:
	docker compose ps -q | xargs docker rm

remove_docker_images:
	docker compose config --images | xargs docker rmi

start:
	docker compose -f docker-compose.yml up --build

start_test:
	docker compose -f docker-compose-test.yml up --build

stop:
	docker compose -f docker-compose-test.yml stop

test:
	. .venv/bin/activate; command cd src; command python -m pytest

start_detached:
	docker compose -f docker-compose-test.yml up --build -d
