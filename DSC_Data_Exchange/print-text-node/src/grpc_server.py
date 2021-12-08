import grpc
from concurrent import futures
import model_pb2
import model_pb2_grpc
import src.print_text_grpc_service as pt


class TextServicer(model_pb2_grpc.PrintTextServicer):
    def print_text(self, request, context):
        print("print_text got called with:")
        print(request.text)
        return model_pb2.Empty()


def start_server(host: str, port: int):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    model_pb2_grpc.add_PrintTextServicer_to_server(TextServicer(), server)
    print("Starting model_grpc Server. Listening on port : " + str(port))
    server.add_insecure_port("{}:{}".format(host, port))
    server.start()
    server.wait_for_termination()