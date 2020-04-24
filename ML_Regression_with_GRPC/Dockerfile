FROM ubuntu:16.04

MAINTAINER Tejas  "tejas.morbagal.harish@iais.fraunhofer.de"

RUN apt-get update -y 
RUN apt-get install -y python3-pip python3-dev 
RUN pip3 install --upgrade pip
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install sklearn
    
COPY ./requirements.txt /requirements.txt
COPY license-1.0.0.json model.proto model_pb2.py model_pb2_grpc.py house_prediction_server.py predict_sale_price.py train.csv test.csv ./

WORKDIR /

RUN pip3 install -r requirements.txt

COPY . /

ENTRYPOINT [ "python3","house_price_prediction_server.py" ]




