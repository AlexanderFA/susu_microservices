import grpc
import reverse_pb2
import reverse_pb2_grpc
from concurrent import futures


class ReverseService(reverse_pb2_grpc.ReverseServiceServicer):
    def ReverseString(self, request, context):
        return reverse_pb2.ReverseResponse(reversed_text=request.text[::-1])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    reverse_pb2_grpc.add_ReverseServiceServicer_to_server(ReverseService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
