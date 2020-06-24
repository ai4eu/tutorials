import grpc
from timeit import default_timer as timer

# import the generated classes
import model_pb2
import model_pb2_grpc

start_ch = timer()

# open a gRPC channel
channel = grpc.insecure_channel('localhost:50051')

# create a stub (client)
stub = model_pb2_grpc.PredictStub(channel)
end_ch = timer()

text = "the movie was a great waste of my time"
ans_lst = []

start = timer()

# create a valid request message
requestPrediction = model_pb2.Text(query = text)

print("Make the call")
# make the call
responsePrediction = stub.classify_review(requestPrediction)


print('The prediction is :', responsePrediction.review)
print('Done!')
