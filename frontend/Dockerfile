FROM node:10.22-alpine
LABEL author="Daniel Ammeraal"

RUN mkdir /frontend
WORKDIR /frontend

COPY package.json /frontend
COPY package-lock.json /frontend
RUN npm install

COPY . /frontend

EXPOSE 3000