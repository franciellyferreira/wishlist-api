settings=wishlist_api.settings.development

ifdef SIMPLE_SETTINGS
	settings=$(SIMPLE_SETTINGS)
else
	export SIMPLE_SETTINGS=$(settings)
endif

export PYTHONPATH=$(shell pwd)/src/
export DJANGO_SETTINGS_MODULE=$(settings)

.PHONY: help

help:  ## This help
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort

install:  ## Install dependencies
	pip install -U -r requirements/dev.txt

safety-check:  ## Search not updated dependencies
	safety check

check:  ## Verify application
	django-admin check

runserver:  ## Run application
	django-admin runserver

migrate:  ## Apply migrations
	django-admin migrate

migrations:  ## Generate migrations
	django-admin makemigrations

create-app:  ## Create new app
	django-admin startapp $(name)
