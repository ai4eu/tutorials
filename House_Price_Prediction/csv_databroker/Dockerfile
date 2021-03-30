FROM ubuntu:20.04

MAINTAINER Tejas  "tejas.morbagal.harish@iais.fraunhofer.de"

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev
RUN pip3 install --upgrade pip
RUN pip3 install numpy
RUN pip3 install pandas

COPY ./requirements.txt /requirements.txt
COPY license-1.0.0.json model.proto model_pb2.py model_pb2_grpc.py csv_server.py get_next_row.py trail.csv ./

WORKDIR /

RUN pip3 install -r requirements.txt

COPY . /

ENTRYPOINT [ "python3","csv_server.py" ]
