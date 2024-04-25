from django.test import TestCase

from utils.tests.base import BaseTestUser
from webchat.models import Conversation, Message
from webchat.serializers import MessageSerializer


class MessageSerializerTest(TestCase, BaseTestUser):
    @classmethod
    def setUpTestData(cls):
        # Create sample data for testing
        cls.user = cls().get_test_active_regularuser()
        cls.conversation = Conversation.objects.create(channel_id="test_channel")
        cls.message_data = {
            "conversation": cls.conversation.id,
            "sender": cls.user.id,
            "content": "new message",
        }

    def test_valid_data(self):
        # Serialize the sample data
        serializer = MessageSerializer(data=self.message_data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)

        # Check that the serialized data matches the input data
        self.assertEqual(
            serializer.validated_data["content"], self.message_data["content"]
        )
        self.assertEqual(
            serializer.validated_data["conversation"].id,
            self.message_data["conversation"],
        )

    def test_get_sender(self):
        # Create a message instance
        message = Message(
            content="test message", sender=self.user, conversation=self.conversation
        )

        # Create a serializer instance
        serializer = MessageSerializer()

        # Call the get_sender method with the message instance
        sender_name = serializer.get_sender(message)

        # Check if the sender's full name matches the expected value
        expected_sender_name = self.user.get_full_name
        self.assertEqual(sender_name, expected_sender_name)

    def test_invalid_data(self):
        # Test with invalid data (missing required field)
        invalid_data = {
            "conversation": self.conversation.id,
            "sender": self.user.id,
        }
        serializer = MessageSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
