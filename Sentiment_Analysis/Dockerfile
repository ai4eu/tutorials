FROM ubuntu:18.04

MAINTAINER Sajid  "sajid.naeem@iais.fraunhofer.de"

RUN apt-get update -y 
RUN apt-get install -y python3-pip python3-dev 
RUN pip3 install --upgrade pip
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install tensorflow==1.13.1

#RUN pip3 install keras
RUN pip3 install keras==2.3.1
RUN pip3 install 'h5py<3.0.0'

COPY ./requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt

RUN useradd app
USER app



COPY license-1.0.0.json model.proto model_pb2.py model_pb2_grpc.py sentiment_analysis_server.py classify_review.py model.h5 train.csv test.csv ./

WORKDIR /

ENTRYPOINT [ "python3","sentiment_analysis_server.py" ]