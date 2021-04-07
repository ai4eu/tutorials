# How to Get an arbitrary Dataset from OpenML and Build a Model


root
<br/>|___classifier
<br/>|___data_node


# 1. Get the data ID from OpenML
Usually whenever opening a dataset in OpenML, the ID is the number at the end of the URL. For instance, the link below contains a dataset with ID 1119. This number will be used to input into the tool.
```
https://www.openml.org/d/1119
```

# 2. Access the Data from OpenML
The source code in folder `data_node` will do the task of retrieving data from openML.

data_node
<br/>|___model.proto
<br/>|___model_pb2.py
<br/>|___model_pb2_grpc.py
<br/>|___myconstants.py
<br/>|___server.py


By inputting the desired and correct data ID into settings as below, you can immediately access data and its labels (if exist), no more action or code modification is needed in this folder `data_node`. Steps are following.

- Replace **DATA_ID** in file ` myconstants.py` with your own dataID. This file is found in both folders `classifier` and `data_node` and both files should be identical so that the communication can be proceeded.

```
DATA_ID = 42563
PORT_ADDRESS = '8061'
PORT_ADDRESS_CLASSIFIER = '8062'
```
This code snippet is for data 42563 (House Price), if you want to access `Adults` data with ID [1119](https://www.openml.org/d/1119), then `DATA_ID = 1119`.
# 3. Get Data and Build the Model
classifier
<br/>|___*classifier_model.proto*
<br/>|___classifier_model_pb2.py
<br/>|___classifier_model_pb2_grpc.py 
<br/>|___classifier_server.py
<br/>|___client.py
<br/>|___model_pb2.py
<br/>|___model_pb2_grpc.py
<br/>|___myconstants.py
<br/>|___utils.py


- All needed functions should be implemented here, in folder `classifier`.

- In this tutorial, 2 available functions `get_feature_names()` and `get_prediction()` are used to get the data column names and predict the samples, respectively. 
- At the client side (`client.py`), for `get_feature_names()`, input message is only the dataID which is already specified in `myconstants.py`.
- For `get_prediction()`, input message is a pair of dataID and samples.
- Depend on your own application and tasks, you can define different types of functions.


Some notes:
- Make sure the values in file `myconstants.py` identical with the one in folder `data_node`.
- In general, only these files below might be modified.
    - classifier_model.proto
    - classifier_server.py
    - client.py
    - myconstants.py

## 3.1. Declare the functions
New functions should be declared in file `classifier_model.proto` under `service Classifier`. 
```
service Classifier {
	rpc GetFeatureNames(DataID) returns (FeatureNames);
    rpc GetPrediction(Request) returns (ClassifierResult);
}
```
You can edit or remove `GetFeatureNames()` and `GetPrediction()`, then add the new ones for your own. 

After the modification, the below command should be run to compile the code and update 2 files `classifier_model_pb2.py` and `classifier_model_pb2_grpc.py `.
```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. classifier_model.proto
```

## 3.2. Implement functions
Under `class ClassifierServicer`, functions in `classifier_model.proto` are implemented. For simplification, the structure sample is written as below.
```
def GetFeatureNames(self, request, context):
    print(f'Request DataID: {request.idx}')
    self._get_data(request)
    return classifier_model_pb2.FeatureNames(feature_names=','.join(self.df.columns))


def GetPrediction(self, request, context):
    idx = request.idx
    value = request.request.split(',')
    self._get_data(request.idx)
    label = self._get_prediction(value)
    return classifier_model_pb2.ClassifierResult(label=str(label))
```        
Currently in this example the private function `_get_data()` is already implemented to get the dataframe and labels (if any) of a dataset with a pre-defined dataID. You can re-use it and don't need to make a new one.
```
def _get_data(self, request):
    # idx = request.idx # fixed when Empty msg sent
    with grpc.insecure_channel(f'localhost:{port_address}') as channel:
        stub = model_pb2_grpc.ExampleStub(channel)
        self.df, self.labels = utils.list_features(stub, idx=idx)
```

## 3.3. Call the functions
In file `client.py`, the request will be defined and sent to the server.
```
def get_feature_names(stub, idx=id_default):
    response = stub.GetFeatureNames(classifier_model_pb2.DataID(idx=idx)).feature_names
    return response


def get_prediction(stub, features):
    idx = features[0]
    request = ','.join([str(i) for i in features[1]])
    response = stub.GetPrediction(classifier_model_pb2.Request(idx=
                                    classifier_model_pb2.DataID(idx=idx),
                                    request=request)).label
    return response
```

# 4. Test the application
- Open one Terminal and cd to folder `data_node`, run 

``` 
python server.py
```
- Open another Terminal and cd to folder `classifier`, run 
```
python classifier_server.py
```
- Open the third Terminal and cd to folder `classifier`, run 
```
python client.py
```

<br/> If you have any issue or trouble, please contact `htran@know-center.at`.