# AI4EU Experiments DSC Connection using gRPC
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
This example is a Machine Learning Regression example that lets clients get the house
sales prediction based on chosen attributes.

# steps
1. Write the service to be served.
2. Make a proto file to define the messages and services.
3. Use the proto file to generate gRPC classes for Python.
4. Create the server.
5. Create the client.
6. Include a license
7. Prepare the docker file, run the docker and the run the client in a new tab.

## Step 1: Write the Service:
In our case, the service is to load the Data. Below is code snippet. To better use the DSC we use the connectorAPI from https://github.com/International-Data-Spaces-Association/DataspaceConnector that also is provided in this repository

```python
from src.connectorAPI.idsapi import IdsApi
from src.connectorAPI.resourceapi import ResourceApi


def get_text(conf):
    consumer_url = conf.custom_dsc if conf.use_custom_dsc else "https://localhost:8080"
    consumer = IdsApi(consumer_url)

    response = consumer.contractRequest(
        conf.provider_url_downloading, conf.resource_id, conf.artifact_id, False, conf.contract
    )

    agreement = response["_links"]["self"]["href"]
    consumer_resources = ResourceApi(consumer_url)
    artifacts = consumer_resources.get_artifacts_for_agreement(agreement)
    first_artifact = artifacts["_embedded"]["artifacts"][0]["_links"]["self"]["href"]
    data = consumer_resources.get_data(first_artifact).text
    print(data)

    return data
```

We pass the service a conf object which holds the information about what data should get downloaded. For better encapsulation of this information we use the below configuration class as a singleton.

```python
class Configuration:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Configuration, cls).__new__(cls)
        return cls.instance

    recipient = None
    resource_id = None
    artifact_id = None
    contract = None
    custom_dsc = None

    use_custom_dsc = False

    data_send = False
```

## Step 2: Make the Proto File:
To implement the service as a gprc service we first need to describe its interface in our model.proto file 
```proto
syntax = 'proto3';

message Text {
  string text = 1;
}

message Empty {

}

service IDSTextConnector {
  rpc get_text(Empty) returns(Text);
}
```


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
python3 -m pip install grpcio-tools googleapis-common-protos
```

* Now, run the following command:
```commandline
python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. model.proto
```
This command used model.proto file to generate the needed stubs to create the
client/server.
The files generated will be as follows:

model_pb2.py — contains message classes

* model_pb2.Features for the input features
* model_pb2.Prediction for the prediction price

model_pb2_grpc.py — contains server and client classes

* model_pb2_grpc.PredictServicer will be used by the server
* model_pb2_grpc.PredictStub the client will use it

## Step 4: Creating the Server:

The server will import the generated files and the function that will handle the
predictions. Then we will define a class that will take a request from the client and
uses the prediction function to return a respond. The request gives us the five
features, the response is a prediction.
After that, we will use add_PredictServicer_to_server function from (model_pb2_grpc.py)
file that was generated before to add the class PredictSevicer to the server.
Once you have implemented all the methods, the next step is to start up a gRPC
server so that clients can actually use your service.
The gRPC server is expected to run on port 8061
The optional HTTP-Server for a Web-UI for human interaction is expected to run on
port 8062.
Below is the house_sale_prediction_client.py

```python
import grpc
from concurrent import futures
import model_pb2
import model_pb2_grpc
import src.dsc_grpc_service as dgs
from src.state.configuration_state import Configuration


class TextServicer(model_pb2_grpc.IDSTextConnectorServicer):
    conf:Configuration = None

    def get_text(self, request, context):
        response = model_pb2.Text()
        if self.conf.data_send:
            self.conf.data_send = False
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('All available data has been processed')
        else:
            self.conf.data_send = True
            response.text = dgs.get_text(self.conf)
        return response


def start_server(port: int, conf):
    print("starting grpc server")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = TextServicer()
    servicer.conf = conf
    model_pb2_grpc.add_IDSTextConnectorServicer_to_server(servicer, server)
    print("Starting model_grpc Server. Listening on port : " + str(port))
    server.add_insecure_port("[::]:{}".format(port))
    server.start()

    return server
```

## Step 5: Write the web-server

To Configure the Node with all its needed Data, we write a REST api, that listens on the same Port as the web-ui. This is just a proof of concept and the configuration could be done in other ways. For example, we could also write a grpc service to implement the configuration directly into the pipeline. 

```python
import os.path
import pprint

from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_marshmallow import Marshmallow
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

from src.dsc_grpc_service import get_text
from src.state.configuration_state import Configuration, get_jsonifyed_configuration

template_dir = os.path.abspath('templates')
app = Flask(__name__, template_folder=template_dir)
ma = Marshmallow(app)
conf = None


class HppInputForm(FlaskForm):
    recipient_str = StringField('Recipient', validators=[DataRequired(), ])
    resource_id_str = StringField('Resource Id', validators=[DataRequired(), ])
    artifact_id_str = StringField('Artifact Id', validators=[DataRequired(), ])
    contract_input_str = StringField('Contract', validators=[DataRequired(), ])

    custom_consumer_toggle = BooleanField('Use Custom Consumer')
    custom_consumer_str = StringField('Custom Consumer')

    submit = SubmitField('Submit Configuration')


class PullForm(FlaskForm):
    submit = SubmitField('Pull Data')


@app.route('/api/v1/recipient', methods=["POST"])
def set_recipient():
    conf.recipient = request.get_json()['recipient']
    pprint.pprint(conf.recipient)
    return get_jsonifyed_configuration()


@app.route('/api/v1/resourceId', methods=["POST"])
def set_resource_id():
    conf.resource_id = request.get_json()['resourceId']
    return get_jsonifyed_configuration()


@app.route('/api/v1/artifactId', methods=["POST"])
def set_artifact_id():
    conf.artifact_id = request.get_json()['artifactId']
    return get_jsonifyed_configuration()


@app.route('/api/v1/download', methods=["POST"])
def set_download():
    conf.download = request.get_json()['download']
    return get_jsonifyed_configuration()


@app.route('/api/v1/contract', methods=["POST"])
def set_contract():
    conf.contract = request.get_json()['contract']
    return get_jsonifyed_configuration()


@app.route('/api/v1/useCustomDSC', methods=["POST"])
def set_use_custom_dsc():
    conf.use_custom_dsc = request.get_json()['useCustomDSC']
    return get_jsonifyed_configuration()


@app.route('/api/v1/data', methods=["GET"])
def get_data():
    data = get_text(conf)
    return data


@app.route('/api/v1/customDSC', methods=["POST"])
def set_custom_dsc():
    conf.custom_dsc = request.get_json()['customDSC']
    return get_jsonifyed_configuration()


@app.route('/', methods=["GET", "POST"])
@app.route('/hpp_input', methods=["GET", "POST"])
def index():
    form = HppInputForm()
    pull_form = PullForm()

    if pull_form.submit.data and pull_form.validate_on_submit():
        return render_template("index.html", form=form, data=get_text(conf), current_configuration=Configuration(),
                               pull_form=pull_form)

    if form.submit.data and form.validate_on_submit():
        print('processing User Input')
        conf.recipient = form.recipient_str.data
        conf.resource_id = form.resource_id_str.data
        conf.artifact_id = form.artifact_id_str.data
        conf.contract = form.contract_input_str.data
        conf.use_custom_dsc = form.custom_consumer_toggle.data
        conf.custom_dsc = form.custom_consumer_str.data

        return render_template("index.html", form=form, current_configuration=Configuration(), pull_form=pull_form)

    return render_template('index.html', form=form, current_configuration=Configuration(), pull_form=pull_form)


def run_flask_app(host: str, port: int, p_conf):
    global conf
    conf = p_conf

    app.secret_key = "dscmodel"
    bootstrap = Bootstrap(app)
    app.app_context().push()
    app.run(host=host, port=port)
```

## Step 6: Creating the Client:

For the implementation of a test client pleas have a look at the test-scripts folder.

## Step 7: Include a license File
We need to include a license file before building a docker image. 

## Step 8: Prepare the Docker file
In the Dockerfile, we download the DataspaceConnector version 6.5.0 and build it. This Dataspace Connector is used by default, if no other is provided as consumer. To run the DSC we then use the openjdk:11 where we install the needed Python version.
```dockerfile
FROM maven:3-jdk-11 As dataspace-connector
WORKDIR /app
RUN curl -LO https://github.com/International-Data-Spaces-Association/DataspaceConnector/archive/refs/tags/v6.5.0.zip
RUN unzip v6.5.0.zip
WORKDIR /app/DataspaceConnector-6.5.0
RUN mvn -e -B dependency:resolve
RUN mvn -e -B dependency:resolve-plugins
RUN mvn -e -B clean package -DskipTests

FROM openjdk:11
WORKDIR /app
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY model.proto /app/model.proto
RUN python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. model.proto

COPY src /app/src/
COPY static /app/static/
COPY templates /app/templates/
COPY app.py /app/app.py
COPY run.sh /app/run.sh
COPY --from=dataspace-connector /app/DataspaceConnector-6.5.0/target/*.jar /app/dataspaceconnector.jar

RUN useradd app
USER app
ENTRYPOINT ["/app/run.sh"]
```

The used requirements.txt:
```requirements.txt
Bootstrap-Flask==1.5.2
Flask==1.1.2
Flask-SQLAlchemy==2.5.1
Flask-WTF==0.14.3
flask-marshmallow==0.14.0
google==3.0.0
googleapis-common-protos==1.53.0
grpcio==1.38.0
grpcio-tools==1.38.0
Jinja2==2.11.3
protobuf==3.16.0
PyYAML==5.4.1
requests==2.25.1
SQLAlchemy==1.4.7
threadpoolctl==2.2.0
urllib3==1.26.5
Werkzeug==1.0.1
WTForms==2.3.3
```

The used run.sh:
```shell
#!/bin/bash

java -jar /app/dataspaceconnector.jar &
python3 -u app.py
```

Build the docker image

```commandline
docker build -t dsc-text-ai4eu:v1 .
```

Run the docker image

```commandline
docker run -p 8061:8061 --rm -ti dsc-text-ai4eu:v1 /bin/bash
```
The -p option maps the port on the container to the host.
The Docker run internally executes house_price_prediction_server.py.
Open one more terminal and run the client which now can access the docker server

```commandline
python3 house_price_prediction_client.py
```

