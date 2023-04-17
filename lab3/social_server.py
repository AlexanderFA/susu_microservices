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
        self.comments = []
        self.likes = []

    def create_message(self, user_id, text):
        message = social_pb2.Message()
        message.message_id = self.message_id
        message.user_id = user_id
        message.text = text
        return message

    def PostMessage(self, request, context):
        message = self.create_message(request.user_id, request.text)
        self.messages.append(message)
        self.message_id += 1
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

    # def CreateUser(self, request, context):
    #     user_id = request.user_id
    #     if user_id in self.users:
    #         context.set_details(f"User {user_id} already exists")
    #         context.set_code(grpc.StatusCode.ALREADY_EXISTS)
    #         return social_pb2.CreateUserResponse(success=False)
    #     self.users[user_id] = request.name
    #     return social_pb2.CreateUserResponse(success=True)
    #
    # def CreatePost(self, request, context):
    #     post_id = len(self.posts) + 1
    #     user_id = request.user_id
    #     if user_id not in self.users:
    #         context.set_details(f"User {user_id} does not exist")
    #         context.set_code(grpc.StatusCode.NOT_FOUND)
    #         return social_pb2.CreatePostResponse(success=False)
    #     post = social_pb2.Post(id=post_id, user_id=user_id, text=request.text)
    #     self.posts[post_id] = post
    #     return social_pb2.CreatePostResponse(success=True, post_id=post_id)
    #
    # def GetPosts(self, request, context):
    #     user_id = request.user_id
    #     if user_id not in self.users:
    #         context.set_details(f"User {user_id} does not exist")
    #         context.set_code(grpc.StatusCode.NOT_FOUND)
    #         return social_pb2.GetPostsResponse(success=False)
    #     user_posts = [post for post in self.posts.values() if post.user_id == user_id]
    #     return social_pb2.GetPostsResponse(success=True, posts=user_posts)
    #
    # def GetPost(self, request, context):
    #     post_id = request.post_id
    #     if post_id not in self.posts:
    #         context.set_details(f"Post {post_id} does not exist")
    #         context.set_code(grpc.StatusCode.NOT_FOUND)
    #         return social_pb2.GetPostResponse(success=False)
    #     post = self.posts[post_id]
    #     return social_pb2.GetPostResponse(success=True, post=post)
    #
    # def CreateComment(self, request, context):
    #     comment_id = len(self.comments) + 1
    #     user_id = request.user_id
    #     post_id = request.post_id
    #     if user_id not in self.users:
    #         context.set_details(f"User {user_id} does not exist")
    #         context.set_code(grpc.StatusCode.NOT_FOUND)
    #         return social_pb2.CreateCommentResponse(success=False)
    #     if post_id not in self.posts:
    #         context.set_details(f"Post {post_id} does not exist")
    #         context.set_code(grpc.StatusCode.NOT_FOUND)
    #         return social_pb2.CreateCommentResponse(success=False)
    #     comment = social_pb2.Comment(
    #         id=comment_id,
    #         user_id=user_id,
    #         post_id=post_id,
    #         text=request.text,
    #     )
    #     self.comments[comment_id] = comment
    #     return social_pb2.CreateCommentResponse(success=True, comment_id=comment_id)
    #
    # def GetComments(self, request, context):
    #     post_id = request.post_id
    #     if post_id not in self.posts:
    #         context.set_details(f"Post {post_id} does not exist")
    #         context.set_code(grpc.StatusCode.NOT_FOUND)
    #         return social_pb2.GetPostResponse(success=False)
    #     post = self.posts[post_id]
    #     return social_pb2.GetPostResponse(success=True, post=post)
    #
    #     post = self.posts.get(request.post_id)
    #     if not post:
    #         context.set_code(grpc.StatusCode.NOT_FOUND)
    #         context.set_details('Post not found')
    #         return social_network_pb2.CommentsResponse()
    #
    #     comments = post.comments
    #     return social_network_pb2.CommentsResponse(comments=comments)

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