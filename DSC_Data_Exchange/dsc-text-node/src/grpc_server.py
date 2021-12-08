import grpc
from concurrent import futures
import model_pb2
import model_pb2_grpc
import src.dsc_grpc_service as dgs
from src.state.configuration_state import Configuration


class TextServicer(model_pb2_grpc.IDSTextConnectorServicer):
    conf:Configuration = None

    def get_text(self, request, context):
        response = model_pb2.Text()
        if self.conf.data_send:
            self.conf.data_send = False
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('All available data has been processed')
        else:
            self.conf.data_send = True
            response.text = dgs.get_text(self.conf)
        return response


def start_server(port: int, conf):
    print("--------------------------------------")
    print("--------------------------------------")
    print("starting grpc server")
    print("--------------------------------------")
    print("--------------------------------------")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = TextServicer()
    servicer.conf = conf
    model_pb2_grpc.add_IDSTextConnectorServicer_to_server(servicer, server)
    print("Starting model_grpc Server. Listening on port : " + str(port))
    server.add_insecure_port("[::]:{}".format(port))
    server.start()

    return server
