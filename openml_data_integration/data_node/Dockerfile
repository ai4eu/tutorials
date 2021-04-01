FROM python:3.8

MAINTAINER HanTran  "htran@know-center.at"


RUN pip install --upgrade pip
RUN pip install pandas
RUN pip install openml
RUN pip install sklearn
    
COPY requirements.txt requirements.txt
COPY license-1.0.0.json model.proto model_pb2.py model_pb2_grpc.py server.py myconstants.py ./

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python", "server.py"]