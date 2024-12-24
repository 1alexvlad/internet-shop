FROM python:3.9-alpine3.16

RUN apk add --no-cache postgresql-client build-base postgresql-dev gettext

COPY requirements.txt /code/requirements.txt
COPY . /code/

WORKDIR /code

EXPOSE 8000

RUN apk add postgresql-client build-base postgresql-dev
RUN pip install -r /code/requirements.txt
RUN adduser --disabled-password service-user