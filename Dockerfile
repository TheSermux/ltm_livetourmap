FROM python:3.9-buster

#RUN apk update   
RUN mkdir /usr/src/app

WORKDIR /usr/src/app
COPY ./requirements.txt .

#RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m spacy download ru_core_news_md

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .
CMD ["gunicorn","--chdir", "solution", "--bind", "0.0.0.0:8000", "backend.manage:app"]
