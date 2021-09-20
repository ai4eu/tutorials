import grpc
from timeit import default_timer as timer
import logging

# import the generated classes
import model_pb2
import model_pb2_grpc

port = 8061


def run(text):
    logging.basicConfig()
    print("Calling HPP_Stub..")
    with grpc.insecure_channel('localhost:{}'.format(port)) as channel:
        stub = model_pb2_grpc.sentiment_analysis_modelStub(channel)
        ui_request = model_pb2.Text(query=text)
        response = stub.classify_review(ui_request)

    print("Greeter client received: ")
    print(response)
    return response.review


if __name__ == '__main__':
    logging.basicConfig()
    text = "the movie was awesome"
    run(text)
