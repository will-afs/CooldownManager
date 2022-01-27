# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP="flaskapp"
ENV FLASK_ENV="prod"

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]