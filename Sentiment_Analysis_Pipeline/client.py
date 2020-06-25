import grpc
from random import randint
from timeit import default_timer as timer

# import the generated classes
import model_pb2
import model_pb2_grpc

import prediction_model_pb2
import prediction_model_pb2_grpc



start_ch = timer()
port_addr = 'localhost:31707'

port_addr1 = 'localhost:32377'

if __name__ == '__main__':
    # open a gRPC channel
    channel = grpc.insecure_channel(port_addr)
    # create a stub (client)
    stub = model_pb2_grpc.get_next_rowStub(channel)

    request_nextrow = model_pb2.Empty()

    next_row = model_pb2.Features

    next_row = (stub.get_next_row(request_nextrow))

    if not str(next_row):
        print('File is finished : ')
    else:
        print('Review is : ', next_row.text)

        # open a gRPC channel #
        channel = grpc.insecure_channel(port_addr1)
        # create a stub (client)
        stub = prediction_model_pb2_grpc.sentiment_analysis_modelStub(channel)

        # create a valid request message
        requestPrediction = prediction_model_pb2.Text(query=next_row.text)

        # make the call
        responsePrediction = stub.classify_review(requestPrediction)

        print('The prediction is :', responsePrediction.review)
        print('Done!')
