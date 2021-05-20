FROM python:3

RUN mkdir /service
COPY . /service/databroker
WORKDIR /service/databroker

RUN apt-get update -y 
RUN apt-get install -y python3-pip python3-dev 
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN useradd app
USER app

ENTRYPOINT [ "python3","-u","server.py" ]
