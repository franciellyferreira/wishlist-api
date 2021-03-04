settings=wishlist.settings.development

ifdef SIMPLE_SETTINGS
	settings=$(SIMPLE_SETTINGS)
else
	export SIMPLE_SETTINGS=$(settings)
endif

export PYTHONPATH=$(shell pwd)/src/
export DJANGO_SETTINGS_MODULE=$(settings)


install:
	pip install -U -r requirements/dev.txt

safety-check:
	safety check

check:
	django-admin check

runserver:
	django-admin runserver

migrate:
	django-admin migrate

migrations:
	django-admin makemigrations
