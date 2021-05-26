FROM python:3.7-slim-buster

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

ENTRYPOINT export FLASK_APP=hello.py && flask run --host 0.0.0.0
