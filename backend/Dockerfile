FROM python:3.7-alpine
LABEL author="Daniel Ammeraal"

ENV PYTHONUNBUFFERED 1

RUN mkdir /backend
WORKDIR /backend
COPY ./requirements.txt /backend/requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /backend/requirements.txt
RUN apk del .tmp-build-deps

COPY . /backend

EXPOSE 8000

RUN adduser -D user
USER user