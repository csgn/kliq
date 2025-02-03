NAME := kliq
TAG=$(shell cat version | awk '{gsub("\\.", ""); print}')
PROJECT_NAME := $(NAME)-$(TAG)
PROJECT_DIR := $(PWD)
DEPLOYMENT_DIR := $(PROJECT_DIR)/docker
ENV_DIR := $(DEPLOYMENT_DIR)/env
CMD := docker compose
COMPOSE_ENTRYPOINT := $(DEPLOYMENT_DIR)/compose.yml

env := $(shell find $(ENV_DIR) -maxdepth 1 -type f -iname "*.env" -exec basename {} .env \; | sed ':a;N;$$!ba;s/\n/ | /g')

ifndef ENV
    $(error ENV does not specified. Example Usage: ENV=($(env)) make up)
else
    ENV_FILE := $(ENV_DIR)/$(ENV).env
endif

ifeq ("$(wildcard $(ENV_FILE))", "")
    $(error '$(ENV)' does not exist. Try ($(env)))
endif

PRE_FLAGS := --file $(COMPOSE_ENTRYPOINT) 				\
			 --project-name $(PROJECT_NAME) 			\
			 --project-directory $(DEPLOYMENT_DIR)		\
			 --env-file $(ENV_FILE)
POST_FLAGS := --build --detach


up:
	$(CMD) $(PRE_FLAGS) up $(POST_FLAGS)

down:
	$(CMD) $(PRE_FLAGS) down

stop:
	$(CMD) $(PRE_FLAGS) stop

summary:
	$(CMD) $(PRE_FLAGS) config
