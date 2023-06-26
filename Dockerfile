FROM python:3.9-alpine

# Disable output buffering
ENV PYTHONBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

ENV DJANGO_SETTINGS_MODULE=flashcards.settings

EXPOSE 8000
