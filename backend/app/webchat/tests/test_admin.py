from django.test import Client, TestCase
from django.urls import reverse

from utils.tests.base import BaseTestUser
from webchat.models import Conversation, Message


class ConversationAdminTestCase(TestCase, BaseTestUser):
    """Test Suit for the Conversation admin"""

    def setUp(self):
        self.client = Client()
        self.admin_user = self.get_test_superuser()
        self.client.force_login(self.admin_user)
        self.conversation = Conversation.objects.create(channel_id="test_channel")

    def test_admin_accessible_conversation(self):
        url = reverse("admin:webchat_conversation_changelist")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.conversation.channel_id)

    def test_edit_conversation_page(self):
        url = reverse("admin:webchat_conversation_change", args=(self.conversation.id,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = {
            "channel_id": "updated_channel_id",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        updated_conversation = Conversation.objects.get(id=self.conversation.id)
        self.assertEqual(updated_conversation.channel_id, data["channel_id"])

    def test_create_conversation_page(self):
        url = reverse("admin:webchat_conversation_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = {
            "channel_id": "new_channel_id",
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(
            Conversation.objects.filter(channel_id=data["channel_id"]).exists()
        )

    def test_conversation_search(self):
        url = (
            reverse("admin:webchat_conversation_changelist")
            + "?q="
            + self.conversation.channel_id
        )
        response = self.client.get(url)
        self.assertContains(response, self.conversation.channel_id)


class MessageAdminTestCase(TestCase, BaseTestUser):
    """Test Suit for the Message admin"""

    @classmethod
    def setUpTestData(cls):
        cls.user = cls().get_test_active_regularuser()
        cls.conversation = Conversation.objects.create(channel_id="test_channel")

    def setUp(self):
        self.client = Client()
        self.admin_user = self.get_test_superuser()
        self.client.force_login(self.admin_user)
        self.message = Message.objects.create(
            conversation=self.conversation, sender=self.user, content="Hello"
        )

    def test_admin_accessible_message(self):
        # "conversation", "sender", "created", "modified"
        url = reverse("admin:webchat_message_changelist")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, "conversation")
        self.assertContains(res, "sender")
        self.assertContains(res, "created")
        self.assertContains(res, "modified")

    def test_edit_message_page(self):
        url = reverse("admin:webchat_message_change", args=(self.message.id,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = {
            "conversation": self.conversation.id,
            "sender": self.user.id,
            "content": "Updated message",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        updated_message = Message.objects.get(id=self.message.id)
        self.assertEqual(updated_message.content, data["content"])

    def test_create_message_page(self):
        url = reverse("admin:webchat_message_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = {
            "conversation": self.conversation.id,
            "sender": self.user.id,
            "content": "New message",
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(Message.objects.filter(content=data["content"]).exists())

    def test_message_search(self):
        url = reverse("admin:webchat_message_changelist") + "?q=" + self.message.content
        response = self.client.get(url)
        self.assertContains(response, self.message.content)
