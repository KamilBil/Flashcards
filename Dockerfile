FROM python:3.11-alpine

# Avoid __pycache__
ENV PYTHONDONTWRITEBYTECODE 1
# Disable output buffering
ENV PYTHONBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . ./

ENV DJANGO_SETTINGS_MODULE=flashcards.settings

EXPOSE 8000

CMD ["gunicorn", "flashcards.wsgi:application", "--bind", "0.0.0.0:8000"]
