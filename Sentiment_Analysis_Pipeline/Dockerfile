FROM ubuntu:16.04

MAINTAINER Sajid  "Sajid.Naeem@iais.fraunhofer.de"

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev
RUN pip3 install --upgrade pip
RUN pip3 install numpy
RUN pip3 install pandas

COPY ./requirements.txt /requirements.txt
COPY license-1.0.0.json model.proto model_pb2.py model_pb2_grpc.py client.py Server.py DataSource.py movies_dataset.csv ./

WORKDIR /

RUN pip3 install -r requirements.txt

COPY . /

EXPOSE 50059
ENTRYPOINT [ "python3","Server.py" ]
