FROM ubuntu:18.04

MAINTAINER Sajid  "sajid.naeem@iais.fraunhofer.de"

RUN apt-get update -y 
RUN apt-get install -y python3-pip python3-dev
RUN pip3 install --upgrade pip
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install tensorflow==2.4.1

RUN pip3 install keras
    
COPY requirements.txt ./requirements.txt
COPY static ./static
COPY templates ./templates
COPY app.py license-1.0.0.json model.h5 model.proto model_pb2.py model_pb2_grpc.py sentiment_analysis_server.py model.py ./

 
WORKDIR /

RUN pip3 install -r requirements.txt

EXPOSE 8061 8062

ENTRYPOINT [ "python3","sentiment_analysis_server.py" ]

