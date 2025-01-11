FROM python:3.12
ENV PYTHONUNBUFFERED=1

#RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./app /app
COPY ./etc /etc
