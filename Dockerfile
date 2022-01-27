# syntax=docker/dockerfile:1

FROM ubuntu:latest
RUN apt-get -y update
RUN apt-get -y install git

FROM python:3.8-slim-buster

WORKDIR /

COPY requirements.txt requirements.txt

ENV PATH="/home/myuser/.local/bin:${PATH}"
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP="flaskapp"
ENV FLASK_ENV="PROD"

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]