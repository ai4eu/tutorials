FROM ubuntu:20.04

MAINTAINER Sajid  "Sajid.Naeem@iais.fraunhofer.de"

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev
RUN pip3 install --upgrade pip
RUN pip3 install numpy
RUN pip3 install pandas
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

RUN useradd app
USER app

COPY license-1.0.0.json databroker.proto databroker_pb2.py databroker_pb2_grpc.py csv_server.py get_next_row.py trail.csv ./

WORKDIR /
COPY . /

ENTRYPOINT [ "python3","-u","csv_server.py" ]
