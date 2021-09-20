import grpc
from concurrent import futures
import threading
import logging

# import the generated classes :
import model_pb2
import model_pb2_grpc
from app import app_run

# import the function we made :
import predict_sale_price as psp
port = 8061
results = []
# create a class to define the server functions, derived from


class PredictServicer(model_pb2_grpc.PredictServicer):
    def predict_sale_price(self, request, context):
        # define the buffer of the response :
        response = model_pb2.Prediction()
        # get the value of the response by calling the desired function :
        response.salePrice = psp.predict_sale_price(request.MSSubClass, request.LotArea, request.YearBuilt, request.BedroomAbvGr, request.TotRmsAbvGrd)
        result = [request.MSSubClass, request.LotArea, request.YearBuilt, request.BedroomAbvGr, request.TotRmsAbvGrd, response.salePrice]
        with open("results.txt", mode="a+") as f:
            # for e0, e1, e2, e3, e4, e5 in result:
            f.write(str(round(request.MSSubClass, 2)) + "|" + str(round(request.LotArea, 2)) + "|" + str(round(request.YearBuilt, 2)) + "|" + str(round(request.BedroomAbvGr, 2)) + "|" + str(round(request.TotRmsAbvGrd, 2)) + "|" + str(round(response.salePrice, 2)) + "\n")
            f.close()
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_pb2_grpc.add_PredictServicer_to_server(PredictServicer(), server)
    server.add_insecure_port('[::]:{}'.format(port))
    server.start()
    threading.Thread(target=app_run()).start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    open('results.txt', 'w').close()
    serve()
