FROM python:3.11-alpine

# Avoid __pycache__
ENV PYTHONDONTWRITEBYTECODE 1
# Disable output buffering
ENV PYTHONBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . ./

ENV DJANGO_SETTINGS_MODULE=flashcards.settings

EXPOSE 8000
