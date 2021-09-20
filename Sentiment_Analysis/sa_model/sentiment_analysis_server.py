import grpc
from concurrent import futures
import threading
import logging

# import the generated classes :
import model_pb2
import model_pb2_grpc
from app import app_run

# import the function we made :
import model as psp
port = 8061
results = []
# create a class to define the server functions, derived from


class sentiment_analysis_modelServicer(model_pb2_grpc.sentiment_analysis_modelServicer):
    def classify_review(self, request, context):
        # define the buffer of the response :
        response = model_pb2.Review_Classify()
        # get the value of the response by calling the desired function :
        response.review = psp.classify_review(request.query)
        result = [request.query, response.review]
        with open("results.txt", mode="a+") as f:
            # for e0, e1, e2, e3, e4, e5 in result:
            f.write(str(request.query) + "|" + str(response.review) + "\n")
            f.close()
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_pb2_grpc.add_sentiment_analysis_modelServicer_to_server(sentiment_analysis_modelServicer(), server)
    server.add_insecure_port('[::]:{}'.format(port))
    server.start()
    threading.Thread(target=app_run()).start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    open('results.txt', 'w').close()
    serve()
