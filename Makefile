.PHONY: install test run

all: install test

install:
	pip install -r requirements/development.txt

test:
	python manage.py test

run:
	sass --watch ./isnts/static/isnts/sass:isnts/static/isnts/css &
	python manage.py makemigrations
	python manage.py migrate
	python manage.py loaddata auth.permission.json auth.group.json bloodtypes.json regions.json towns.json ntssus.json
	python manage.py runserver
