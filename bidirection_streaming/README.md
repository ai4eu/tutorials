# This is a feature that is not yet available in the AI4EU Experiments Platform but planned to be implemented soon.
# BidirectionalStreaming 
**Expected behavior:** 
- Client streams sensor data from 4 sensors with `id` for each measurement. The server receives the streams and do some balck box processing and then streams back the respective `id` and a prediction value. 
- For every one measurement the client sends the server should send back one processed value without any delay. 
## Overview
- `boker.proto` defines the data strcuture for the communication

    - The `BrokerRequest` message definition specifies five fields. Each field has a name and a tyoe. The numbers are not values for the fields. They only indicate the order of serializing the fields. 
    - The `BrokerResponse` message definition specifies two fields.
    - To use the message types with an RPC (Remote Procedure Call) system, you can define an RPC service interface in a ``.proto`` file and the protocol buffer compiler will generate service interface code and stubs in your chosen language. 
    - The RPC service defined here takes ``BrokerRequest`` as request and returns ``BrokerResponse``. 

- To generate python classes for the `broker.proto` file, I have created a shell script. It creates a ``server`` and ``client`` directory and then creates the python classes inside it. It also creates the ``server/server.py`` and ``client/client.py`` file for you. Just run the shell script and relax.
````
sh generate_proto.sh
````
````
Then enter the name of proto file
````
## Generated class
### ``databroker_pb2.py`` - contains message classes
- **databroker_pb2.Features** for sending response
- **databroker_pb2.Empty** for sending request
### ``databroker_pb2_grpc.py`` - contains server and client classes
- **databroker_pb2_grpc.BidirectionalStreamingServicer** will be used by server
- **databroker_pb2_grpc.BidirectionalStreamingStub** will be used by client

## Server
- The gRPC server will run on port 8061
## Docker
Build the docker image
````
docker build -t databroker:v2 .
````
Run the docker image
````
docker run -p 8061:8061 --rm -ti databroker:v2 /bin/bash
````
On another terminal run the client
````
python3 client.py
````
## Repository structure
````
.
├── client
│   ├── client.py
│   ├── config.py
│   ├── databroker_pb2_grpc.py
│   ├── databroker_pb2.py
│   ├── __pycache__
│   └── requirements.txt
├── databroker
│   ├── config.py
│   ├── databroker_pb2_grpc.py
│   ├── databroker_pb2.py
│   ├── dockerfile
│   ├── __pycache__
│   ├── requirements.txt
│   └── server.py
├── dataset
│   └── sensors.csv
├── protobufs
│   └── databroker.proto
├── README.md
└── requirements.txt
````
## Securing Client Server Communication
- First we create a self signed certificate using `openssl`. To so that run this command
````
sh generate_certificate.sh
````
- At this stage, you will have two files: ``server.key`` and ``server.crt``. 
- On the server side, we will need both these files; on the client side, we will only need the ``server.crt`` file.

## Implementing server side gRPC interceptors
- Interceptors are custom code that run on servers and clients during a request/response lifecycle.