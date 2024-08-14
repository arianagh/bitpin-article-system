server:
	python3 manage.py runserver --settings=core.settings.development


db: makemigrations migrate


makemigrations:
	python3 manage.py makemigrations


migrate:
	python3 manage.py migrate

test:
	python3 manage.py test


beat:
	celery -A core.celery beat -l info


celery:
	celery -A core.celery worker -l info


requirements:
	pip install -r requirements.txt
