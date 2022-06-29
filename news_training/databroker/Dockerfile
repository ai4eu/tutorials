FROM python:3.8

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev 
RUN pip3 install --upgrade pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN mkdir /news_databroker
COPY . /news_databroker
WORKDIR /news_databroker

RUN useradd app
USER app

ENTRYPOINT python3 -u news_databroker.py
