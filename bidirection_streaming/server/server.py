import os
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from signal import signal, SIGTERM
import grpc
from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from databroker_pb2 import BrokerResponse
import databroker_pb2_grpc
import config


class BrokerServiceServicer(databroker_pb2_grpc.BrokerServiceServicer):

    def BidirectionalStreaming(self, request_iterator, context):
        """Server request callback function"""
        if not request_iterator:
            raise NotFound("Client request is incorrect!")

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
    interceptors = [ExceptionToStatusInterceptor()]
    server = grpc.server(
            ThreadPoolExecutor(max_workers=10),
            interceptors=interceptors)
    databroker_pb2_grpc.add_BrokerServiceServicer_to_server(
            BrokerServiceServicer(), 
            server)
        # read in key and certificate
    with open(os.path.join(os.path.split(__file__)[0], 'server.key')) as f:
        private_key = f.read().encode()

    with open(os.path.join(os.path.split(__file__)[0], 'server.crt')) as f:
        certificate_chain = f.read().encode()

    # create server credentials
    server_credentials = grpc.ssl_server_credentials( ( (private_key, certificate_chain), ) )
    server.add_secure_port(config.port, server_credentials)

    print("Starting server. Listening on port : " + str(config.port))
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted!")
        exit(0)
