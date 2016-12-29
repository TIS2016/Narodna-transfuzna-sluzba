.PHONY: install test run build

all: install test

build:
	sass --update ./isnts/static/isnts/sass:isnts/static/isnts/css

install:
	pip install -r requirements/development.txt
	gem install sass

test:
	python manage.py test

run:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py loaddata auth.permission.json auth.group.json bloodtypes.json regions.json towns.json ntssus.json nts.json
	python manage.py runserver
