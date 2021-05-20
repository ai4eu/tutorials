import os
import time
import csv
import grpc

from databroker_pb2 import BrokerRequest
from databroker_pb2_grpc import BrokerServiceStub
import config


class Client():
    """
    Client streams rows from a CSV file to the server and receives the response stream.
    """

    def __init__(self, port, credentials):
        channel = grpc.secure_channel(port, credentials)
        self.stub = BrokerServiceStub(channel)
        self.bidirectional_streaming(self.stub)

    def stream_messages(self):
        """Server request callback function"""
        csv_filename = config.csv_file_path
        with open(csv_filename, "r") as dataset:
            row = csv.reader(dataset, delimiter=",")
            for i, data in enumerate(row):
                request = BrokerRequest(id=int(data[0]),
                                        sensor1=float(data[1]),
                                        sensor2=float(data[2]),
                                        sensor3=float(data[3]),
                                        sensor4=float(data[4]))
                yield request
                time.sleep(config.streaming_rate)

    def bidirectional_streaming(self, stub):
        response_iterator = stub.BidirectionalStreaming(self.stream_messages())
        for response in response_iterator:
            print("Server response: ", int(response.id),
                  bool(response.prediction))


def main():
    #with open(os.path.join(os.path.split(__file__)[0], 'server.crt')) as f:
    with open('server.crt') as f:
        credentials = grpc.ssl_channel_credentials(root_certificates=f.read().encode())
    
    Client(config.port, credentials)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted!")
        exit(0)
