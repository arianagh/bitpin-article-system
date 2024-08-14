FROM python:3.10.14-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--reload", "--workers", "3", "--bind", "0.0.0.0:8000",
 "--env", "DJANGO_SETTINGS_MODULE=core.settings.development", "core.wsgi:application"]