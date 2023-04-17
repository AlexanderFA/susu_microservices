import grpc
import social_pb2
import social_pb2_grpc


def post_message(stub, user_id, text):
    post_message_request = social_pb2.PostMessageRequest()
    post_message_request.user_id = user_id
    post_message_request.text = text
    response = stub.PostMessage(post_message_request)
    print("Created message ID is:", response.message_id)


def get_messages(stub, user_id):
    get_messages_request = social_pb2.GetMessagesRequest()
    get_messages_request.user_id = user_id
    response = stub.GetMessages(get_messages_request)
    print("Get messages response:")
    for message in response.messages:
        print(f"Message ID: {message.message_id}\nUser ID: {message.user_id}\nText: {message.text}\nLikes: {message.likes}\n")


def like_message(stub, message_id):
    like_message_request = social_pb2.LikeMessageRequest()
    like_message_request.message_id = message_id
    like_message_response = stub.LikeMessage(like_message_request)
    print("Likes of this message:", like_message_response.likes)


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = social_pb2_grpc.SocialNetworkStub(channel)

    while True:
        command = input("Enter command (post/get/like/comment/quit): ")
        if command == "post":
            user_id = int(input("Enter user ID: "))
            text = input("Enter message text: ")
            post_message(stub, user_id, text)
        elif command == "get":
            user_id = int(input("Enter user ID: "))
            get_messages(stub, user_id)
        elif command == "like":
            message_id = int(input("Enter message ID: "))
            like_message(stub, message_id)
        elif command == "quit":
            break
        else:
            print("Invalid command. Please try again.")


if __name__ == '__main__':
    run()

# def run():
#     with grpc.insecure_channel('localhost:50051') as channel:
#         stub = social_network_pb2_grpc.SocialNetworkStub(channel)
#
#         # Отправляем сообщение
#         message_request = social_network_pb2.MessageRequest(
#             user_id=1,
#             message="Hello, world!"
#         )
#         message_response = stub.PostMessage(message_request)
#         print(f"Message sent with ID: {message_response.message_id}")
#
#         # Получаем ленту сообщений
#         message_stream_request = social_network_pb2.UserRequest(user_id=1)
#         message_stream_response = stub.GetMessageStream(message_stream_request)
#         for message_response in message_stream_response:
#             print(f"Message {message_response.message_id} from User {message_response.user_id}: {message_response.message}")
#             print(f"Timestamp: {message_response.timestamp}")
#             print(f"Likes: {message_response.likes}")
#             print("Comments:")
#             for comment in message_response.comments:
#                 print(f"\tComment {comment.comment_id} from User {comment.user_id}: {comment.comment}")
#                 print(f"\tTimestamp: {comment.timestamp}")
#
#         # Добавляем комментарий к посту
#         comment_request = social_network_pb2.CommentRequest(
#             message_id=1,
#             user_id=2,
#             comment="Great post!"
#         )
#         comment_response = stub.AddComment(comment_request)
#         print(f"Comment added with ID: {comment_response.comment_id}")
#
#         # Получаем комментарии к посту
#         message_id_request = social_network_pb2.MessageIdRequest(message_id=1)
#         comment_response = stub.GetComments(message_id_request)
#         for comment in comment_response.comments:
#             print(f"Comment {comment.comment_id} from User {comment.user_id}: {comment.comment}")
#             print(f"Timestamp: {comment.timestamp}")
#
#         # Лайкаем пост
#         post_id_request = social_network_pb2.PostIdRequest(post_id=1)
#         like_response = stub.LikePost(post_id_request)
#         print(f"Likes: {like_response.likes}")
#
#         # Отменяем лайк поста
#         unlike_response = stub.UnlikePost(post_id_request)
#         print(f"Likes: {unlike_response.likes}")
#
#
