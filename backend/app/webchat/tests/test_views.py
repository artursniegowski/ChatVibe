from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from utils.tests.base import BaseTestUser
from webchat.models import Conversation, Message
from webchat.serializers import MessageSerializer


class MessageViewSetTest(TestCase, BaseTestUser):
    """Test suit for MessageViewSet"""

    @classmethod
    def setUpTestData(cls) -> None:
        # creating sample data for testing
        cls.user = cls().get_test_active_regularuser()
        cls.channel_id = "550e8400-e29b-41d4-a716-446655440000"
        cls.conversation = Conversation.objects.create(channel_id=cls.channel_id)
        cls.msg_one = Message.objects.create(
            conversation=cls.conversation, sender=cls.user, content="Message One"
        )
        cls.msg_two = Message.objects.create(
            conversation=cls.conversation, sender=cls.user, content="Message Two"
        )

    def setUp(self) -> None:
        # initialize the test client
        self.client = APIClient()

    def test_list_messages_all(self):
        url = reverse("webchat:webchat-messages-list")
        response = self.client.get(url, {"by_channelId": self.channel_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # messages = self.conversation.message.all()
        messages = Message.objects.filter(conversation__channel_id=self.channel_id)
        serializer_data = MessageSerializer(messages, many=True).data
        self.assertEqual(response.data, serializer_data)

    def test_list_messages_without_channel_id(self):
        url = reverse("webchat:webchat-messages-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_messages_with_not_found_channel_id_format(self):
        url = reverse("webchat:webchat-messages-list")
        not_existing_channel_id = "550e8400-e29b-41d4-a716-446655440002"
        response = self.client.get(url, {"by_channelId": not_existing_channel_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])
