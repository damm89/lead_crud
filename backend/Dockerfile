FROM python:3.7-alpine
LABEL author="Daniel Ammeraal"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /backend
WORKDIR /backend
COPY . /backend

EXPOSE 8000

RUN adduser -D user
USER user