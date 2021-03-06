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

clean: ## Clean local environment
	@find . -name "*.pyc" | xargs rm -rf
	@find . -name "*.pyo" | xargs rm -rf
	@find . -name "__pycache__" -type d | xargs rm -rf
	@rm -f .coverage
	@rm -rf htmlcov/
	@rm -f coverage.xml
	@rm -f *.log

install:  ## Install dependencies
	pip install -U -r requirements/dev.txt

safety-check:  ## Search not updated dependencies
	safety check

check:  ## Verify application
	django-admin check

create-app:  ## Create new app
	django-admin startapp $(name)

runserver:  ## Run application
	django-admin runserver

migrate:  ## Apply migrations
	django-admin migrate

migrations:  ## Generate migrations
	django-admin makemigrations

test: clean  ## Run tests
	pytest -x

test-coverage: clean ## Calculate all test coverage
	pytest -x --cov=src/wishlist_api/ --cov-config=.coveragerc --cov-report=xml --cov-report=term-missing

test-coverage-html: clean ## Calculate all test coverage and generate report html
	pytest -x --cov=src/wishlist_api/ --cov-config=.coveragerc --cov-report=html:htmlcov

generate-key:  ## Generate secret key
	python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
