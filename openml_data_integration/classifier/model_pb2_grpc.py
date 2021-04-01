# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import model_pb2 as model__pb2


class ExampleStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.PullData = channel.unary_stream(
                '/know_center.openml.example.Example/PullData',
                request_serializer=model__pb2.Empty.SerializeToString,
                response_deserializer=model__pb2.Response.FromString,
                )


class ExampleServicer(object):
    """Missing associated documentation comment in .proto file."""

    def PullData(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ExampleServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'PullData': grpc.unary_stream_rpc_method_handler(
                    servicer.PullData,
                    request_deserializer=model__pb2.Empty.FromString,
                    response_serializer=model__pb2.Response.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'know_center.openml.example.Example', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Example(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def PullData(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/know_center.openml.example.Example/PullData',
            model__pb2.Empty.SerializeToString,
            model__pb2.Response.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
