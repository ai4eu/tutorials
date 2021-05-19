import time
import csv
import grpc

from databroker_pb2 import BrokerRequest
from databroker_pb2_grpc import BrokerServiceStub
import config

PORT = config.localhost
STREAM_RATE = config.streaming_rate
PATH = config.csv_file_path


class Client():
    """
    Client streams rows from a CSV file to the server and receives the response stream.
    """

    def __init__(self):
        channel = grpc.insecure_channel(PORT)
        self.stub = BrokerServiceStub(channel)
        self.bidirectional_streaming(self.stub)

    def stream_messages(self):
        """Server request callback function"""
        csv_filename = PATH
        with open(csv_filename, "r") as dataset:
            row = csv.reader(dataset, delimiter=",")
            for i, data in enumerate(row):
                request = BrokerRequest(id=int(data[0]),
                                        sensor1=float(data[1]),
                                        sensor2=float(data[2]),
                                        sensor3=float(data[3]),
                                        sensor4=float(data[4]))
                yield request
                time.sleep(STREAM_RATE)

    def bidirectional_streaming(self, stub):
        response_iterator = stub.BidirectionalStreaming(self.stream_messages())
        for response in response_iterator:
            print("Server response: ", int(response.id),
                  bool(response.prediction))


def main():
    Client()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted!")
        exit(0)
