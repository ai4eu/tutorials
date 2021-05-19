from concurrent import futures
from threading import Thread
import grpc

from databroker_pb2 import BrokerResponse
import databroker_pb2_grpc
import config

PORT = config.port

class BrokerServiceServicer(databroker_pb2_grpc.BrokerServiceServicer):

    def BidirectionalStreaming(self, request_iterator, context):
        """Server request callback function"""
        for request in request_iterator:
            print("Client request: ",
                  request.id,
                  request.sensor1,
                  request.sensor2,
                  request.sensor3,
                  request.sensor4)
            if (request.id % 2) == 0:
                yield BrokerResponse(id=request.id, prediction=True)
            else:
                yield BrokerResponse(id=request.id, prediction=False)


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    databroker_pb2_grpc.add_BrokerServiceServicer_to_server(
        BrokerServiceServicer(), server)
    print("Starting server. Listening on port : " + str(PORT))
    server.add_insecure_port("[::]:{}".format(PORT))
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted!")
        exit(0)
