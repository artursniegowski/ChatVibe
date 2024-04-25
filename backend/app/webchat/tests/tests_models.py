from django.core.exceptions import ValidationError
from django.db.utils import DataError, IntegrityError
from django.test import TestCase

from utils.tests.base import BaseTestUser
from webchat.models import Conversation, Message


class ConversationModelTest(TestCase):
    """Test suit for Conversation Model."""

    def test_max_length_name(self):
        # Attempt to create a Category with a name longer than 100 characters
        max_length = Conversation._meta.get_field("channel_id").max_length
        long_channel_id = "a" * (max_length + 1)
        with self.assertRaises(DataError):
            Conversation.objects.create(channel_id=long_channel_id)

    def test_conversation_str_representation(self):
        conversation = Conversation.objects.create(channel_id="test_channel")
        self.assertEqual(str(conversation), "test_channel")


class MessageModelTest(TestCase, BaseTestUser):
    """Test suit for Message Model."""

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = cls().get_test_active_regularuser()
        cls.conversation = Conversation.objects.create(channel_id="test_channel")

    def test_create_message(self):
        message = Message.objects.create(
            conversation=self.conversation, sender=self.user, content="Hello"
        )
        self.assertEqual(message.content, "Hello")

    def test_message_requires_conversation(self):
        with self.assertRaises(IntegrityError) as context:
            Message.objects.create(sender=self.user, content="Hello")
        # Check if the exception message contains information about the conversation constraint
        self.assertIn("conversation", str(context.exception))

    def test_message_requires_sender(self):
        with self.assertRaises(IntegrityError) as context:
            Message.objects.create(conversation=self.conversation, content="Hello")
        # Check if the exception message contains information about the sender constraint
        self.assertIn("sender", str(context.exception))

    def test_message_requires_content(self):
        # Message.objects.create(conversation=self.conversation, sender=self.user)
        message = Message(conversation=self.conversation, sender=self.user)
        with self.assertRaises(ValidationError) as context:
            message.full_clean()
        # Check if the exception message contains information about the content constraint
        self.assertIn("content", str(context.exception))

    def test_message_conversation_relationship(self):
        message = Message.objects.create(
            conversation=self.conversation, sender=self.user, content="Hello"
        )
        self.assertIn(message, self.conversation.message.all())

    def test_message_deletion_on_user_deletion(self):
        # Ensure messages are deleted when associated user is deleted
        message = Message.objects.create(
            conversation=self.conversation, sender=self.user, content="Hello"
        )
        self.assertIn(message, self.conversation.message.all())
        user_id = self.user.id
        self.user.delete()
        self.assertFalse(Message.objects.filter(sender_id=user_id).exists())

    def test_message_deletion_on_conversation_deletion(self):
        # Ensure messages are deleted when associated conversation is deleted
        message = Message.objects.create(
            conversation=self.conversation, sender=self.user, content="Hello"
        )
        self.assertIn(message, self.conversation.message.all())
        conversation_id = self.conversation.id
        self.conversation.delete()
        self.assertFalse(
            Message.objects.filter(conversation_id=conversation_id).exists()
        )
