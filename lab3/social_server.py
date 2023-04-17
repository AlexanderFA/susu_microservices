from concurrent import futures
import grpc
import time
import social_pb2
import social_pb2_grpc
from concurrent import futures
import random


class SocialNetworkServicer(social_pb2_grpc.SocialNetworkServicer):
    def __init__(self):
        self.messages = []
        self.message_id = 1
        self.comment_id = 1
        self.comments = []
        self.likes = []

    def create_message(self, user_id, text):
        message = social_pb2.Message()
        message.message_id = self.message_id
        message.user_id = user_id
        message.text = text
        self.message_id += 1
        return message

    def PostMessage(self, request, context):
        message = self.create_message(request.user_id, request.text)
        self.messages.append(message)
        return social_pb2.PostMessageResponse(message_id=message.message_id)

    def GetMessages(self, request, context):
        response = social_pb2.GetMessagesResponse()
        for message in self.messages:
            if message.user_id == request.user_id:
                response.messages.append(message)
        return response

    def LikeMessage(self, request, context):
        response = social_pb2.LikeMessageResponse()
        message_id = request.message_id
        try:
            message_ind = message_id - 1
            names = ["Alice", "Bob", "Charlie", "Dave", "Eve", "Frank"]
            random_name = random.choice(names)
            self.messages[message_ind].likes.append(random_name.encode('utf-8'))
            response.likes.extend(self.messages[message_ind].likes)
        except IndexError:
            print("No such message.")

        return response

    def create_comment(self, user_id, text):
        comment = social_pb2.Comment()
        comment.comment_id = self.comment_id
        comment.user_id = user_id
        comment.text = text
        self.comment_id += 1
        return comment

    def AddComment(self, request, context):
        response = social_pb2.AddCommentResponse()
        comment = self.create_comment(request.user_id, request.text)

        message_id = request.message_id
        try:
            message_ind = message_id - 1
            self.messages[message_ind].comments.append(comment)
            print(self.messages[message_ind].comments)
        except IndexError:
            print("No such message.")

        return social_pb2.AddCommentResponse(comment_id=comment.comment_id)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    social_pb2_grpc.add_SocialNetworkServicer_to_server(SocialNetworkServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started. Listening on port 50051.")
    try:
        while True:
            # time.sleep(86400)
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()