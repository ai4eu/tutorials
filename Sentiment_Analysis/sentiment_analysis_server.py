import grpc
from concurrent import futures
import time

# import the generated classes :
import model_pb2
import model_pb2_grpc

# import the function we made :
import model as psp

port = 8061


# create a class to define the server functions, derived from
# usingSKlearn_pb2_grpc.PredictServicer :
class sentiment_analysis_modelServicer(model_pb2_grpc.sentiment_analysis_modelServicer):
    def classify_review(self, request, context):
        # define the buffer of the response :
        response = model_pb2.Review_Classify()
        # get the value of the response by calling the desired function :
        response.review = psp.classify_review(request.query)
        return response


# creat a grpc server :
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

model_pb2_grpc.add_sentiment_analysis_modelServicer_to_server(sentiment_analysis_modelServicer(), server)

print('Starting server. Listening on port :' + str(port))
server.add_insecure_port("[::]:{}".format(port))
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
