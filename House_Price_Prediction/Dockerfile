FROM ubuntu:18.04

MAINTAINER Tejas  "tejas.morbagal.harish@iais.fraunhofer.de"

RUN apt-get update -y 
RUN apt-get install -y python3-pip python3-dev 
RUN pip3 install --upgrade pip
RUN pip3 install numpy
RUN pip3 install pandas
RUN pip3 install sklearn
WORKDIR /
COPY ./requirements.txt /requirements.txt
RUN pip3 install -r requirements.txt

RUN useradd app
USER app
COPY license-1.0.0.json model.proto model_pb2.py model_pb2_grpc.py house_price_prediction_server.py predict_sale_price.py train.csv test.csv ./
COPY . /

ENTRYPOINT [ "python3","-u","house_price_prediction_server.py" ]




