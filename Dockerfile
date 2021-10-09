FROM python:3.9-buster

#RUN apk update   
RUN mkdir /usr/src/app

WORKDIR /usr/src/app
COPY ./requirements.txt .


# set environment variables
ENV PYTHONDONTWRITEBYTECODE i
ENV PYTHONUNBUFFERED 1

#RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m spacy download ru_core_news_md

COPY . .
