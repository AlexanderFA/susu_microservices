import grpc
import time
import social_pb2
import social_pb2_grpc
from concurrent import futures


class SocialNetworkServicer(social_pb2_grpc.SocialNetworkServicer):
    def __init__(self):
        self.messages = []
        self.message_id = 0

    def PostMessage(self, request, context):
        message = social_pb2.Message()
        message.message_id = self.message_id
        message.user_id = request.user_id
        message.text = request.text
        self.messages.append(message)
        self.message_id += 1
        return social_pb2.PostMessageResponse(success=True)

    def GetMessages(self, request, context):
        response = social_pb2.GetMessagesResponse()
        for message in self.messages:
            if message.user_id == request.user_id:
                response.messages.append(message)
        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    social_pb2_grpc.add_SocialNetworkServicer_to_server(SocialNetworkServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started. Listening on port 50051.")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
