# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import model_pb2 as model__pb2


class IDSTextConnectorStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.get_text = channel.unary_unary(
                '/IDSTextConnector/get_text',
                request_serializer=model__pb2.Empty.SerializeToString,
                response_deserializer=model__pb2.Text.FromString,
                )


class IDSTextConnectorServicer(object):
    """Missing associated documentation comment in .proto file."""

    def get_text(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_IDSTextConnectorServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'get_text': grpc.unary_unary_rpc_method_handler(
                    servicer.get_text,
                    request_deserializer=model__pb2.Empty.FromString,
                    response_serializer=model__pb2.Text.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'IDSTextConnector', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class IDSTextConnector(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def get_text(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/IDSTextConnector/get_text',
            model__pb2.Empty.SerializeToString,
            model__pb2.Text.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
