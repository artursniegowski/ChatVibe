from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth import get_user_model

from server.models import Server
from webchat.models import Conversation, Message

User = get_user_model()


class WebChatConsumer(JsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_id = None
        self.user = None

    def connect(self):
        self.user = self.scope.get("user")
        # the middlewre wil be called eveytime we try making a new web scoket connection
        # adding authentication of the user before actully connecting
        # grabing the token, and trying to validate it - this will be done
        # in the custom middleware
        # and now we can check if the user is logged in
        if not self.user or not self.user.is_authenticated:
            # closing the connection
            self.close(code=4001)
            return

        self.accept()

        # getting the channel id
        self.channel_id = self.scope["url_route"]["kwargs"]["channel_id"]
        # getting the server id
        self.server_id = self.scope["url_route"]["kwargs"]["server_id"]

        # setting the user that makes the connection as the current user
        # self.user = User.objects.get(id=self.user.id)
        # this is done alredy from the scope

        # now we can determine if the user with the give user id is a member ot not
        # getting first the server
        server = Server.objects.get(id=self.server_id)
        # checking if the user is a member
        # and now this can eb used in the receive_json method
        self.is_member = server.member.filter(id=self.user.id).exists()

        # https://channels.readthedocs.io/en/latest/topics/channel_layers.html#synchronous-functions
        async_to_sync(self.channel_layer.group_add)(
            self.channel_id,
            self.channel_name,
        )

    def receive_json(self, content=None, bytes_data=None):
        # called when the consumer recives the message
        # content -> this is the recived message

        # limiting the user from seding a message if the user is not a member
        if not self.is_member:
            return

        channel_id = self.channel_id
        sender = self.user
        message = content["message"]

        obj, is_created = Conversation.objects.get_or_create(channel_id=channel_id)

        new_message = Message.objects.create(
            conversation=obj,
            sender=sender,
            content=message,
        )

        async_to_sync(self.channel_layer.group_send)(
            # using group send to send messages to all channelsin a particular group
            self.channel_id,
            # this is the message we are sending
            {
                "type": "chat.message",
                "new_message": {
                    "id": str(new_message.id),
                    "sender": new_message.sender.get_full_name,
                    "content": new_message.content,
                    "created": new_message.created.isoformat(),
                },
            },
        )

    def chat_message(self, event):
        # sending the message
        # it is a consumer method which is invoked when a message of type chat.message
        # is received by the consumer
        self.send_json(event)

    def disconnect(self, close_code):
        # Called when the socket closes
        # try to remove the user that disconnects
        async_to_sync(self.channel_layer.group_discard)(
            self.channel_id, self.channel_name
        )
        super().disconnect(close_code)
