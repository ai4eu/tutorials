# AI4EU Experiments Onboarding Tutorial: Sentiment Analysis using gRPC
This tutorial provides a basic Python programmer’s introduction to working with gRPC.
By walking through this example you’ll learn how to:
* Define a service in a .proto file.
* Generate server and client code using the protocol buffer compiler.
* Use the Python gRPC API to write a simple client and server for your service.

It assumes that you have read the Overview(https://grpc.io/docs/guides/#overview) and are familiar with protocol buffers.(https://developers.google.com/protocol-buffers/docs/overview)
You can find out more in the proto3 language guide and Python generated code guide.
(https://developers.google.com/protocol-buffers/docs/reference/python-generated)

# What is gRPC?
With gRPC you can define your service once in a .proto file and implement clients and
servers in any of gRPC’s supported languages, which in turn can be run in
environments ranging from servers inside Google to your own tablet - all the
complexity of communication between different languages and environments is
handled for you by gRPC. You also get all the advantages of working with protocol
buffers, including efficient serialization, a simple IDL, and easy interface updating.
This example is a Machine Learning Classification example that lets clients get the house
result and precision.

# steps
1. Write the service to be served.
2. Make a proto file to define the messages and services.
3. Use the proto file to generate gRPC classes for Python.
4. Create the server.
5. Create the client.
6. Include a license
7. Prepare the docker file, run the docker and the run the client in a new tab.

## Step 1: Write the Service:
In our case, the service is predicting house pricing. Below is code snippet.

```python
from keras.preprocessing import sequence
from keras.datasets import imdb
from keras.models import load_model

def classify_review(review):
	maxlen = 100
	model = load_model('model.h5')
	d = imdb.get_word_index()
	words = review.split()
	review = []
	for word in words:
		if word not in d:
			review.append(2)
		else:
			review.append(d[word] + 3)

	review = sequence.pad_sequences([review], truncating='pre', padding='pre', maxlen=maxlen)
	prediction = model.predict(review)
	return prediction[0][0]
```
This model has 1 input arguments the review of the user and return the value where as 1 mean positive and 0 mean negative.
Since our motive here is to understand the gRPC, I have taken a simple classification example from sklearn.

## Step 2: Make the Proto Files, First one is for databroker and Second one is for Sentiment Analysis :

```proto
//Define the used version of proto
syntax = 'proto3';

message Features {
    float row_Number     = 1 ;
    string user_review   = 2 ;
    float polarity       = 3 ;

}

message Empty {
}

service get_next_row {
    rpc get_next_row(Empty) returns(Features);
}
```


```proto
//Define the used version of proto
syntax = "proto3";


//Define a message to hold the features input by the client
message Features {
    float row_Number     = 1 ;
    string user_review   = 2 ;
    float polarity       = 3 ;

}
//Define a message to hold the predicted price
message Prediction {
    float review      = 1 ;
}

//Define the service
service Predict {
    rpc predict_sentiment_analysis(Features) returns (Prediction);
}
```
Here, we did not give values to the features, those numbers indicate the order of serializing
the features.

## Step 3: Generate gRPC classes for Python:

Open the terminal, change the directory to be in the same folder that the proto file is
in.
To generate the gRPC classes we have to install the needed libraries first:

* Install gRPC :
```cmd
python3 -m pip install grpcio
```

* To install gRPC tools, run:
```commandline
python3 -m pip install grpcio-tools googleapis-commonprotos
```

* Now, run this command inside csv_databroker folder:
```commandline
python3 -m grpc_tools.protoc -I. --python_out=. --
grpc_python_out=. databroker.proto
```

* Now, run this command inside Sentiment_Analysis Command:
```commandline
python3 -m grpc_tools.protoc -I. --python_out=. --
grpc_python_out=. model.proto
```
This command used model.proto file to generate the needed stubs to create the
client/server.
The files generated will be as follows:

model_pb2.py — contains message classes

* model_pb2.Features for the input features
* model_pb2.Prediction for the prediction review

model_pb2_grpc.py — contains server and client classes

* model_pb2_grpc.PredictServicer will be used by the server
* model_pb2_grpc.PredictStub the client will use it

## Step 4: Creating the Server:

The server will import the generated files and the function that will handle the
predictions. Then we will define a class that will take a request from the client and
uses the prediction function to return a respond. The request gives us the one
features, the response is a prediction.
After that, we will use add_PredictServicer_to_server function from (model_pb2_grpc.py)
file that was generated before to add the class PredictSevicer to the server.
Once you have implemented all the methods, the next step is to start up a gRPC
server so that clients can actually use your service.
The gRPC server is expected to run on port 8061
The optional HTTP-Server for a Web-UI for human interaction is expected to run on
port 8062.
Below is the sentiment_analysis_server.py

```python
import grpc
from concurrent import futures
import time

# import the generated classes :
import model_pb2
import model_pb2_grpc

# import the function we made :
import classify_review as psp
port = 8061

# create a class to define the server functions, derived from

class PredictServicer(model_pb2_grpc.PredictServicer):
    def predict_sentiment_analysis(self, request, context):
        # define the buffer of the response :
        response = model_pb2.Prediction()
        # get the value of the response by calling the desired function :
        response.review = psp.classify_review(request.user_review)
        return response


# creat a grpc server :
server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10))

model_pb2_grpc.add_PredictServicer_to_server(PredictServicer(), server)

print("Starting server. Listening on port : " + str(port))
server.add_insecure_port("[::]:{}".format(port))
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
```

## Step 5: Creating the Client:

In the client file we will do the following:
* Open a gRPC channel
* Create a stub
* Create a request message
* Use the stub to call the service

Below is the code snippet for client:

```python
import grpc
from random import randint
from timeit import default_timer as timer

# import the generated classes
import model_pb2
import model_pb2_grpc


start_ch = timer()
port_address = 'localhost:8061'
# open a gRPC channel
channel = grpc.insecure_channel(port_address)

# create a stub (client)
stub = model_pb2_grpc.PredictStub(channel)
end_ch = timer()

text = "the movie was a great waste of my time"
ans_lst = []

start = timer()

# create a valid request message
requestPrediction  = model_pb2.Features(user_review = text)

print("Make the call")
# make the call
responsePrediction = stub.predict_sentiment_analysis(requestPrediction)

print("Prediction (0 = negative, 1 = positive) = ", end="")

print('The prediction is :',responsePrediction.review)
print('Done!')
```

## Step 6: Include a license File
We need to include a license file before building a docker image. 

## Step 7: Prepare the Docker files, first one is for databroker and second one is sentiment analysis
```dockerfile
ROM ubuntu:20.04

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
```


```dockerfile
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
```

In the docker file, we copy the license file along with other files required to the
container.
Whenever any layer is re-built all the layers that follow it in the Dockerfile need to be
rebuilt too. It's important to keep this fact in mind while creating Dockerfiles.
The dockerfile here separates out the gRPC specific requirements in a separate file
called requirements.txt. The reason for doing this is to separate the application
dependency from the gRPC dependency. gRPC dependency in requirements.txt will be
built as a separate layer when the Docker image is built. This avoids rebuild of this
layer every time a change is made in the application. Below is the contents of gRPC
requirement.txt.

```requirements.txt
# GRPC Python setup requirements
coverage>=4.0
cython>=0.29.8
enum34>=1.0.4
protobuf>=3.5.0.post1
six>=1.10
wheel>=0.29
grpcio-tools

```

Build the docker image inside sentiment_analysis folder

```commandline
docker build -t sentiment_analysis:v1 .
```
Run the docker image

```commandline
docker run -p 8061:8061 --rm -ti sentiment_analysis:v1 /bin/bash
```

Build the docker image inside csv_databroker folder

```commandline
docker build -t csv_databroker_sentiment_analysis:v1 .
```

Run the docker image

```commandline
docker run -p 8061:8061 --rm -ti csv_databroker_sentiment_analysis:v1 /bin/bash
```

The -p option maps the port on the container to the host.
The Docker run internally executes sentiment_analysis_server.py and csv_server.
Open one more terminal and run the clients which now can access the docker server

```commandline
python3 sentiment_analysis_client.py
```

```commandline
python3 csv_client.py
```
