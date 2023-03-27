import grpc
import social_pb2
import social_pb2_grpc


def post_message(stub, user_id, text):
    post_message_request = social_pb2.PostMessageRequest()
    post_message_request.user_id = user_id
    post_message_request.text = text
    response = stub.PostMessage(post_message_request)
    print("Post message response:", response)


def get_messages(stub, user_id):
    get_messages_request = social_pb2.GetMessagesRequest()
    get_messages_request.user_id = user_id
    response = stub.GetMessages(get_messages_request)
    print("Get messages response:")
    for message in response.messages:
        print(f"Message ID: {message.message_id}\nUser ID: {message.user_id}\nText: {message.text}\n")


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = social_pb2_grpc.SocialNetworkStub(channel)

    while True:
        command = input("Enter command (post/get/quit): ")
        if command == "post":
            user_id = int(input("Enter user ID: "))
            text = input("Enter message text: ")
            post_message(stub, user_id, text)
        elif command == "get":
            user_id = int(input("Enter user ID: "))
            get_messages(stub, user_id)
        elif command == "quit":
            break
        else:
            print("Invalid command. Please try again.")


if __name__ == '__main__':
    run()
