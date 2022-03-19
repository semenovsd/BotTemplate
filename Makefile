SHELL := /bin/bash
PYTHON ?= python
DOCKER_COMPOSE ?= docker-compose.yml
MANAGE_PY ?= web/manage.py
COMMIT ?= No comment

include .env

help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

pull: ## Git pull updates
	git pull

push: ## Git push updates
	git add --all
	git commit -m "$(COMMIT)"
	git push

docker-install: # Download & Install % Start Docker
	sudo apt-get update
	sudo apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common
	curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
	sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
	sudo apt-get update
	sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose
	sudo systemctl start docker

	# Enable userns-remap on the daemon
	sudo echo "{ \"userns-remap\": \"default\" }" > /etc/docker/daemon.json
	sudo systemctl restart docker

docker_without_sudo: # Add group docker
	-@sudo groupadd docker
	sudo usermod -aG docker ${USER}
	newgrp docker
	#sudo chmod ug+s /usr/bin/docker
	#sudo chown $USER /var/run/docker.sock

docker-check:  ## Check docker containers
	docker ps -q | xargs  docker stats --no-stream

create_certs:  ## Make ssl certificates
	mkdir "${SSL_DIR}"
	openssl req -newkey rsa:2048 -sha256 -nodes -keyout "${SSL_DIR}${SSL_PRIV}" -out "${SSL_DIR}${SSL_CERT}" \
	-x509  -days 365 -subj "/C=US/ST=Oregon/L=Portland/O=Company Name/OU=Org/CN=${DOMAIN_NAME_OR_IP}"
	sudo chmod -R +r "${SSL_DIR}"

build: ## Build the project (Install docker, addgroup, make ssl certs)
	make docker-install
	make docker_without_sudo
	make create_certs

down: ## Down & remove containers
	docker-compose -f $(DOCKER_COMPOSE) down

stop: ## Stop containers
	docker-compose -f $(DOCKER_COMPOSE) stop

start: ## Restart containers
	make stop
	-make pull
	docker-compose -f $(DOCKER_COMPOSE) up --build
