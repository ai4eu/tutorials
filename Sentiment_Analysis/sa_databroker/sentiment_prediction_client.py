import grpc
from timeit import default_timer as timer
import logging

# import the generated classes
import model_pb2
import model_pb2_grpc

port = 8061


def run():
    print("Calling HPP_Stub..")
    with grpc.insecure_channel('localhost:{}'.format(port)) as channel:
        stub = model_pb2_grpc.DatabrokerStub(channel)
        ui_request = model_pb2.Empty()
        response = stub.sadatabroker(ui_request)

    print("Greeter client received: ")
    print(response)


if __name__ == '__main__':
    logging.basicConfig()
    run()
