import grpc
from timeit import default_timer as timer
import logging

# import the generated classes
import model_pb2
import model_pb2_grpc

port = 8061


def run(hpp_parameters):
    logging.basicConfig()
    print("Calling HPP_Stub..")
    start_ch = timer()
    with grpc.insecure_channel('localhost:{}'.format(port)) as channel:
        stub = model_pb2_grpc.PredictStub(channel)
        ui_request = model_pb2.Features(MSSubClass=float(hpp_parameters[0]), LotArea=float(hpp_parameters[1]),
                                        YearBuilt=float(hpp_parameters[2]), BedroomAbvGr=float(hpp_parameters[3]),
                                        TotRmsAbvGrd=float(hpp_parameters[4])
                                        )
        response = stub.predict_sale_price(ui_request)

    print("Greeter client received: ")
    print(response)
    end_ch = timer()
    print('Done!')
    ch_time = end_ch - start_ch
    print('Time for connecting to server = {}'.format(ch_time))
    return response.salePrice


if __name__ == '__main__':
    logging.basicConfig()
    parameters = [5.5, 2.0, 2.5, 1.8, 4]
    run(parameters)
