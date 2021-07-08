FROM python:3.8

WORKDIR /tensorboard

RUN apt-get update -y 
RUN apt-get install -y python3-pip python3-dev 
RUN pip3 install --upgrade pip
RUN pip3 install tensorflow

RUN useradd app
USER app

ENTRYPOINT tensorboard --port=8062 --logdir=$SHARED_FOLDER_PATH --bind_all
