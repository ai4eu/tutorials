import grpc
import model_pb2
import model_pb2_grpc

port_addr = 'localhost:8061'

channel = grpc.insecure_channel(port_addr)

stub = model_pb2_grpc.IDSTextConnectorStub(channel)

response = stub.get_text(model_pb2.Empty())

print(response.text)