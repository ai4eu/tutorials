FROM ubuntu:20.04

MAINTAINER Raul "raul.saavedra.felipe@iais.fraunhofer.de"

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev
RUN pip3 install --upgrade pip
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install openml
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

WORKDIR /

COPY license-1.0.0.json model.proto model_pb2.py model_pb2_grpc.py server.py openml_data_fetcher.py myconstants.py /

ENTRYPOINT [ "python3","-u","server.py" ]
