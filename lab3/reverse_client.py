import grpc
import reverse_pb2
import reverse_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = reverse_pb2_grpc.ReverseServiceStub(channel)
        response = stub.ReverseString(reverse_pb2.ReverseRequest(text='hello world'))
        print("Reversed string received: " + response.reversed_text)


if __name__ == '__main__':
    run()
