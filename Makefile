.PHONY: install test run

all: install test

install:
	pip install -r requirements/development.txt

test:
	python manage.py test

run:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py loaddata auth.permission.json auth.group.json bloodtypes.json regions.json towns.json ntssus.json nts.json
	python manage.py runserver
