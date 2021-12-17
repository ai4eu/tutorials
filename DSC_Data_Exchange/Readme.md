# AI4EU Experiments DSC Connection using gRPC

This is a simple implementation of the DSC (found here: https://github.com/International-Data-Spaces-Association/DataspaceConnector). For more information about the international dataspaces project plese consult https://internationaldataspaces.org/.

The AI4EU Node described here can be configured to download some text data with one DSC from another DSC. To use the node one has to configure it via the provided REST-api so the node knows which data to download and where to find it. After that the node gives this data to the next node and the pipeline can continue.

## Limitations

Because this is just a simple proof of concept there are known limitations which we want to adress here. 

### Authentication

By now the Node can't be configured with authentication data for the used DSC. It always uses the default (username: admin, password: password).

### grpc configuration

At the moment the configuration can only be done by the provided REST-api. To better integrate the node into the whole grpc flow of AI4EU this configuration could also be done with a grpc service. 

