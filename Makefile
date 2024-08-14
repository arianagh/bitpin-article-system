server:
	python3 manage.py runserver --settings=core.settings.development


run-gunicorn:
	gunicorn --reload --workers 3 --bind 0.0.0.0:8000 --env DJANGO_SETTINGS_MODULE=core.settings.development core.wsgi:application


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
