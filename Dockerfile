# syntax=docker/dockerfile:1

# Set the base image name
FROM ubuntu:latest

# Install the following commands
RUN apt-get -y update
RUN apt-get -y install git

# Set the base image name
FROM python:3.8-slim-buster

# Set the working directory
WORKDIR /

# Copy over the files from the local machine towards the container
COPY . .

# Install Python dependencies
ENV PATH="/home/myuser/.local/bin:${PATH}"
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set Flask environment variables
ENV FLASK_APP="flaskapp"
ENV FLASK_ENV="PROD"

# Run the flask application listening on any IPv4, on port 80
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=80"]