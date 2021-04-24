import grpc
from random import randint
from timeit import default_timer as timer

# import the generated classes
import model_pb2
import model_pb2_grpc


start_ch = timer()
port_address = 'localhost:8061'
# open a gRPC channel
channel = grpc.insecure_channel(port_address)

# create a stub (client)
stub = model_pb2_grpc.PredictStub(channel)
end_ch = timer()

text = "the movie was a great waste of my time"
ans_lst = []

start = timer()

# create a valid request message
requestPrediction  = model_pb2.Features(user_review = text)

print("Make the call")
# make the call
responsePrediction = stub.predict_sentiment_analysis(requestPrediction)

print("Prediction (0 = negative, 1 = positive) = ", end="")

print('The prediction is :',responsePrediction.review)
print('Done!')
