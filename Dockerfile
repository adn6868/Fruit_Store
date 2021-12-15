# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /main

COPY requirements.txt requirements.txt
RUN apt-get update -y 
RUN apt-get install apt-file -y 
RUN apt-get install -y python3-dev build-essential
RUN python3 -m pip install -r requirements.txt

COPY . .
CMD [ "python3", "main.py"]