FROM python:3.7

COPY wait-for-it.sh /bin/wait-for-it
COPY src/requirements.txt /requirements.txt
RUN pip install -r requirements.txt
RUN mkdir /code
WORKDIR /code
