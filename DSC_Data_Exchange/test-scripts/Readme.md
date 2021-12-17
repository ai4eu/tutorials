# Test scipts fot the dsc-text-node

In this folder we provide some scripts to simplify the use of the dsc-text-node for test purposes. 

## fill_provider

This script can be used to create some text data in a DSC. You can provide the DSC to use as first commandline argument (default: "https://localhost:8080") and the data to create as second commandline argument (default: "SOME LONG VALUE")

## grpc_test_client

This script can be used to make a simple gRPC call. To use it, you need to copy it to the dsc-text-node folder because it needs the compiled gRPC classes model_pb2 and model_pb2_grpc there. Then you can simply run it, and it should make the gRPC call and print its output to the commandline.

## configure_node 

This script can be used to configure the dsc-text-node. It searches a provided DSC for Resources, Artifacts and Contracts and simply picks the first to use in the dsc-text-node. To use it one as to provide where to find the REST-api as first commandline argument. If you use the node inside an AI4EU kubernetes cluster you can get the correct address with:

kubectl -n <your-namespace> get node,service,pod -o wide

With this command kubectl should give you all the pods, their ip address and the exposed port. Simply search the webui pod of the dsc-node and you should find its ip address and port. The correct address to give the script then would be http://<webui-ip-address>:<webui-port>

Other commandline arguments you can pass the script are the following in this exact order:

consumer_url_searching (default: "https://localhost:8081"): 
Through this DSC the script communicates with the provider to search for the resources. This is not the same Address as the consumer that downloads the data inside the pipeline. Those two could be different, because one communicates out of a Docker Container and one simply from the host.

provider_url_searching (default: "https://172.17.0.1:8080"):
The DSC address where the script should search for resources. this also isn't the address where the pipeline will download the data, because of communication from within Docker containers.

consumer_url_downloading (default: "https://172.17.0.1:8081"):
The DSC address through which the pipeline will try to communicate with the dataprovider dsc. 

provider_url_downloading (default "https://172.17.0.1:8080/api/ids/data"):
The DSC address where the pipeline will try to download the data from. 


If you have successfully filled the provider dsc and configured the node, the pipeline should be able to communicate with the dsc, download the text data and pass it to the next step inside the pipeline.