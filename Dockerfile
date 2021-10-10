FROM python:3.9-buster

#RUN apk update   
RUN mkdir /usr/src/app

WORKDIR /usr/src/app
COPY ./backend/requirements.txt ./backend/requirements.txt

#RUN pip install --upgrade pip
RUN cd backend && pip install -r requirements.txt
RUN cd backend && python -m spacy download ru_core_news_md

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "backend.manage:app"]
