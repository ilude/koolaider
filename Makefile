.PHONY: run
SITE_PACKAGES := $(shell pip show pip | grep '^Location' | cut -d' ' -f2-)
PROJECT_NAME := $(shell basename $(shell pwd))

# read and include .devcontainer/.env exporting all variables
ifneq (,$(wildcard .devcontainer/.env))
	include .devcontainer/.env
	export
	ENV_FILE = .devcontainer/.env
endif

ifneq (,$(wildcard .env))
	include .env
	export
	ENV_FILE = .env
endif

run: $(SITE_PACKAGES)
	python3 app/app.py

reqs:	$(SITE_PACKAGES)

$(SITE_PACKAGES): requirements.txt
	pip install -r requirements.txt
	touch requirements.txt


build-image:
	docker build --target production -t ghcr.io/ilude/$(PROJECT_NAME):latest .

push-image: build-image
	docker push ghcr.io/ilude/$(PROJECT_NAME)

stop-image:
	-docker stop $(PROJECT_NAME)

run-image: build-image stop-image
	docker run -d -it --rm --env-file $(ENV_FILE) --name $(PROJECT_NAME) ghcr.io/ilude/$(PROJECT_NAME):latest

bash-image: build-image
	docker run -it --rm --env-file $(ENV_FILE) --name $(PROJECT_NAME) ghcr.io/ilude/$(PROJECT_NAME):latest bash

logs:
	docker logs -f $(PROJECT_NAME)

ansible:
	LC_ALL=C.UTF-8 ansible-playbook --inventory 127.0.0.1 --connection=local .devcontainer/ansible/setup-container.yml