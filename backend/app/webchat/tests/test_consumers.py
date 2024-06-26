import sys
import time
from unittest.mock import MagicMock

from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer
from channels.routing import URLRouter
from django.test import AsyncClient, SimpleTestCase
from django.urls import reverse

from app import urls
from server.models import Category, Server
from utils.tests.base import BaseTestUser
from webchat.middleware import JWTAuthMiddleWare
from webchat.models import Conversation, Message

# https://github.com/django/channels/issues/1942
# workaround for needing daphne - uvicorn is used here so should not depend on it
# Mocking channels.testing.live module
sys.modules["channels.testing.live"] = MagicMock()

from channels.testing import WebsocketCommunicator  # noqa E402


# or using TransactionTestCase, without -> databases = '__all__'
class WebChatConsumerTestCase(SimpleTestCase, BaseTestUser):
    databases = "__all__"

    @classmethod
    def setUpClass(cls):
        cls.user = cls().get_test_active_regularuser()
        cls.non_member_user = cls().get_test_staffuser()
        cls.category = Category.objects.create(
            name="Test Category", description="Test Description"
        )
        cls.server = Server.objects.create(
            name="Test server", owner=cls.user, category=cls.category
        )
        cls.server.member.add(cls.user)
        cls.server_id = cls.server.id
        cls.channel_id = "test_channel_id"
        cls.application = JWTAuthMiddleWare(URLRouter(urls.websocket_urlpatterns))
        cls.channel_layer = get_channel_layer()

    # addint this code to setupclass would save testing time but would require
    # adjustment of BaseTestUser to return the test data for users
    # TODO: investinget this further
    async def get_token(self, user, password) -> str:
        """returns token for the given user"""
        client = AsyncClient()
        response = await client.post(
            reverse("token_obtain_pair"),
            data={"email": user.email, "password": password},
        )
        token = response.cookies.get("access_token").value
        return token

    async def get_headers(self, user=None) -> dict:
        """adding headers with tokens as cookie"""
        if not user:  # for regualr user defined in the base class
            user = self.user
            self._get_regularuser_active_data()
            password = self.regularuser_active_data.password
        else:  # for staff user defined in the base class
            self._get_staffuser_data()
            password = self.staffuser_data.password
        token = await self.get_token(user, password)
        headers = {b"cookie": f"access_token={token}".encode()}
        return headers

    async def test_unauthenticated_user_connect(self):
        # Simulate an unauthenticated user by not providing any headers
        headers = {b"cookie": f"access_token={'not.valid.token'}".encode()}
        unique_channel_id = self.channel_id + "test_unauthenticated_user_connect"
        communicator = WebsocketCommunicator(
            self.application,
            f"/ws/{self.server_id}/{unique_channel_id}/",
            headers=headers,
        )
        connected, close_code = await communicator.connect()  # Connect to WebSocket
        self.assertFalse(connected)  # Ensure connection is closed
        # Check if the close code is 4001
        self.assertEqual(
            close_code, 4001
        )  # Check if the expected close code is returned

    async def test_non_member_cannot_send_message(self):
        # Create a user who is not a member of the server
        headers = await self.get_headers(self.non_member_user)
        unique_channel_id = self.channel_id + "non_member_send_message"
        # Connect the WebSocket communicator for the non-member user
        communicator = WebsocketCommunicator(
            self.application,
            f"/ws/{self.server_id}/{unique_channel_id}/",
            headers=headers,
        )
        connected, _ = await communicator.connect()

        # Send a message attempt
        message = {"message": "This message should not be sent"}
        await communicator.send_json_to(message)

        # Check that the consumer did not send any messages
        response = await communicator.receive_nothing()
        self.assertTrue(response)

        # Disconnect the communicator
        await communicator.disconnect()

    async def test_connect_websocket(self):
        # this way the asynchronous test wont mess with other running tests
        headers = await self.get_headers()
        unique_channel_id = self.channel_id + "connect_simple"
        communicator = WebsocketCommunicator(
            self.application,
            f"/ws/{self.server_id}/{unique_channel_id}/",
            headers=headers,
        )
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_disconnect(self):
        # this way the asynchronous test wont mess with other running tests
        headers = await self.get_headers()
        unique_channel_id = self.channel_id + "disconect_simple"
        communicator = WebsocketCommunicator(
            self.application,
            f"/ws/{self.server_id}/{unique_channel_id}/",
            headers=headers,
        )
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        await communicator.disconnect()
        response = await communicator.receive_nothing()
        self.assertTrue(response)  # Ensure no further messages received

    async def test_invalid_url(self):
        headers = await self.get_headers()
        communicator = WebsocketCommunicator(
            self.application, f"/ws/{self.server_id}/", headers=headers
        )  # Missing channel_id
        with self.assertRaises(ValueError):
            connected, subprotocol = await communicator.connect()

    async def test_message_handling_with_message_conversation_creation(self):
        # this way the asynchronous test wont mess with other running tests
        headers = await self.get_headers()
        unique_channel_id = self.channel_id + "conversation"
        communicator = WebsocketCommunicator(
            self.application,
            f"/ws/{self.server_id}/{unique_channel_id}/",
            headers=headers,
        )
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected)

        message = {"message": "Hello, world!"}
        await communicator.send_json_to(message)

        response = await communicator.receive_json_from()
        self.assertIn("new_message", response)  # Ensure message received
        self.assertIn("id", response["new_message"])
        self.assertIn("sender", response["new_message"])
        self.assertIn("content", response["new_message"])
        self.assertIn("created", response["new_message"])
        self.assertEqual(response["new_message"]["content"], message["message"])

        # Check if the conversation was created
        conversation_db = await sync_to_async(
            Conversation.objects.filter(channel_id=unique_channel_id).first
        )()
        self.assertIsNotNone(conversation_db)

        # Check if the message was created and associated with the conversation
        message_db = await sync_to_async(
            Message.objects.filter(conversation=conversation_db).first
        )()
        self.assertIsNotNone(message_db)
        self.assertEqual(message_db.content, message["message"])

        await communicator.disconnect()

    async def test_group_operations(self):
        # this way the asynchronous test wont mess with other running tests
        headers = await self.get_headers()
        unique_channel_id = self.channel_id + "operations"
        communicator1 = WebsocketCommunicator(
            self.application,
            f"/ws/{self.server_id}/{unique_channel_id}/",
            headers=headers,
        )
        communicator2 = WebsocketCommunicator(
            self.application,
            f"/ws/{self.server_id}/{unique_channel_id}/",
            headers=headers,
        )
        connected1, _ = await communicator1.connect()
        self.assertTrue(connected1)
        connected2, _ = await communicator2.connect()
        self.assertTrue(connected2)

        # Send a message from communicator2
        message = {"message": "Hello from communicator2!"}
        await communicator2.send_json_to(message)

        # Ensure communicator1 receives the message
        response = await communicator1.receive_json_from()

        self.assertIn("new_message", response)
        self.assertIn("id", response["new_message"])
        self.assertIn("sender", response["new_message"])
        self.assertIn("content", response["new_message"])
        self.assertIn("created", response["new_message"])
        self.assertEqual(response["new_message"]["content"], message["message"])

        # Disconnect communicator1 and communicator2
        await communicator1.disconnect()
        await communicator2.disconnect()

    async def test_discard_group_on_disconnect(self):
        # Connect multiple clients
        # ensuring that the consumer correctly cleans up after itself when the connection is closed
        # and that the channel name is discarded

        # this way the asynchronous test wont mess with other running tests
        unique_channel_id = self.channel_id + "discard"
        headers = await self.get_headers()
        communicator1 = WebsocketCommunicator(
            self.application,
            f"/ws/{self.server_id}/{unique_channel_id}/",
            headers=headers,
        )
        communicator2 = WebsocketCommunicator(
            self.application,
            f"/ws/{self.server_id}/{unique_channel_id}/",
            headers=headers,
        )
        connected1, _ = await communicator1.connect()
        self.assertTrue(connected1)
        connected2, _ = await communicator2.connect()
        self.assertTrue(connected2)

        # Define a function to clean up expired channels and retrieve channel names
        async def clean_up_and_get_channel_names():
            # Retrieve list of all channel names
            c_key = self.channel_layer._group_key(unique_channel_id)
            c_connection = self.channel_layer.connection(
                self.channel_layer.consistent_hash(unique_channel_id)
            )
            # Discard old channels based on group_expiry
            await c_connection.zremrangebyscore(
                c_key, min=0, max=int(time.time()) - self.channel_layer.group_expiry
            )
            c_names = [
                x.decode("utf8") for x in await c_connection.zrange(c_key, 0, -1)
            ]
            return c_names

        c_names_before_disconnect1 = await clean_up_and_get_channel_names()
        self.assertTrue(len(c_names_before_disconnect1) > 0)

        await communicator1.disconnect()

        c_names_before_disconnect2 = await clean_up_and_get_channel_names()
        self.assertEqual(
            len(c_names_before_disconnect1), len(c_names_before_disconnect2)
        )

        # # Disconnect the other client
        await communicator2.disconnect()

        c_names_after_disconnect2 = await clean_up_and_get_channel_names()
        self.assertEqual(
            len(c_names_before_disconnect1) - 1, len(c_names_after_disconnect2)
        )
