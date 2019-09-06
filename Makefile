SHELL := /bin/bash                                             

ifdef USE_VENV
RUN_CMD = cd src &&
else
RUN_CMD = docker-compose exec django
endif

all: flake8 test

flake8: 
	$(RUN_CMD) flake8

test:
	$(RUN_CMD) pytest

fill-db:
	${RUN_CMD} python manage.py migrate
	${RUN_CMD} python manage.py createsuperuser
	${RUN_CMD} python manage.py loaddata dlp/fixtures/filter_rules.json

clean:
	sudo find src/ -name "*pyc" -delete
	sudo find src/ -name "__pycache__" -delete
