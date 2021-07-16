# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from deephaven.proto import barrage_pb2 as deephaven_dot_proto_dot_barrage__pb2


class BarrageServiceStub(object):
    """
    A barrage service is an endpoint for retrieving or storing ticking Arrow data.
    Implementations should also implement FlightService.
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.DoSubscribe = channel.stream_stream(
                '/io.deephaven.proto.backplane.grpc.BarrageService/DoSubscribe',
                request_serializer=deephaven_dot_proto_dot_barrage__pb2.SubscriptionRequest.SerializeToString,
                response_deserializer=deephaven_dot_proto_dot_barrage__pb2.BarrageData.FromString,
                )
        self.DoSubscribeNoClientStream = channel.unary_stream(
                '/io.deephaven.proto.backplane.grpc.BarrageService/DoSubscribeNoClientStream',
                request_serializer=deephaven_dot_proto_dot_barrage__pb2.SubscriptionRequest.SerializeToString,
                response_deserializer=deephaven_dot_proto_dot_barrage__pb2.BarrageData.FromString,
                )
        self.DoUpdateSubscription = channel.unary_unary(
                '/io.deephaven.proto.backplane.grpc.BarrageService/DoUpdateSubscription',
                request_serializer=deephaven_dot_proto_dot_barrage__pb2.SubscriptionRequest.SerializeToString,
                response_deserializer=deephaven_dot_proto_dot_barrage__pb2.OutOfBandSubscriptionResponse.FromString,
                )


class BarrageServiceServicer(object):
    """
    A barrage service is an endpoint for retrieving or storing ticking Arrow data.
    Implementations should also implement FlightService.
    """

    def DoSubscribe(self, request_iterator, context):
        """
        Create a table subscription. You can send a new request to update the subscription.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DoSubscribeNoClientStream(self, request, context):
        """
        Create a table subscription. This variant is server-side streaming only. This is to better serve javascript clients
        which have poor bidirectional streaming support.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DoUpdateSubscription(self, request, context):
        """
        Update a subscription out-of-band. The provided sequence is used as a high water mark; the server ignores
        requests that do not increase the sequence. It assumes it was a request received out of order.
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BarrageServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'DoSubscribe': grpc.stream_stream_rpc_method_handler(
                    servicer.DoSubscribe,
                    request_deserializer=deephaven_dot_proto_dot_barrage__pb2.SubscriptionRequest.FromString,
                    response_serializer=deephaven_dot_proto_dot_barrage__pb2.BarrageData.SerializeToString,
            ),
            'DoSubscribeNoClientStream': grpc.unary_stream_rpc_method_handler(
                    servicer.DoSubscribeNoClientStream,
                    request_deserializer=deephaven_dot_proto_dot_barrage__pb2.SubscriptionRequest.FromString,
                    response_serializer=deephaven_dot_proto_dot_barrage__pb2.BarrageData.SerializeToString,
            ),
            'DoUpdateSubscription': grpc.unary_unary_rpc_method_handler(
                    servicer.DoUpdateSubscription,
                    request_deserializer=deephaven_dot_proto_dot_barrage__pb2.SubscriptionRequest.FromString,
                    response_serializer=deephaven_dot_proto_dot_barrage__pb2.OutOfBandSubscriptionResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'io.deephaven.proto.backplane.grpc.BarrageService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class BarrageService(object):
    """
    A barrage service is an endpoint for retrieving or storing ticking Arrow data.
    Implementations should also implement FlightService.
    """

    @staticmethod
    def DoSubscribe(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(request_iterator, target, '/io.deephaven.proto.backplane.grpc.BarrageService/DoSubscribe',
            deephaven_dot_proto_dot_barrage__pb2.SubscriptionRequest.SerializeToString,
            deephaven_dot_proto_dot_barrage__pb2.BarrageData.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DoSubscribeNoClientStream(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/io.deephaven.proto.backplane.grpc.BarrageService/DoSubscribeNoClientStream',
            deephaven_dot_proto_dot_barrage__pb2.SubscriptionRequest.SerializeToString,
            deephaven_dot_proto_dot_barrage__pb2.BarrageData.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DoUpdateSubscription(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/io.deephaven.proto.backplane.grpc.BarrageService/DoUpdateSubscription',
            deephaven_dot_proto_dot_barrage__pb2.SubscriptionRequest.SerializeToString,
            deephaven_dot_proto_dot_barrage__pb2.OutOfBandSubscriptionResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
