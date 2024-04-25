from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from django.contrib.auth import get_user_model

from webchat.models import Conversation, Message

User = get_user_model()


class WebChatConsumer(JsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_id = None
        self.user = None

    def connect(self):
        self.accept()
        # getting the channel id
        self.channel_id = self.scope["url_route"]["kwargs"]["channel_id"]

        # TODO: # setting a static user for now, later it will be dynamicly adjsuted
        self.user = User.objects.first()  # this will be the admin user

        # https://channels.readthedocs.io/en/latest/topics/channel_layers.html#synchronous-functions
        async_to_sync(self.channel_layer.group_add)(
            self.channel_id,
            self.channel_name,
        )

    def receive_json(self, content=None, bytes_data=None):
        # called when the consumer recives the message
        # content -> this is the recived message
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
