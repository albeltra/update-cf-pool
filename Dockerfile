FROM python:3.11-alpine

RUN mkdir /scripts

COPY ./update.py /scripts/
