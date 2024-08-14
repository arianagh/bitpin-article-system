FROM python:3.10.14-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "--bind", "--reload", "0.0.0.0:8000", "core.wsgi:application"]
