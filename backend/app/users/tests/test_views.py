from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.serializers import UserSerializer
from utils.tests.base import BaseTestUser

User = get_user_model()


class UserViewSetTest(APITestCase, BaseTestUser):
    """Test suite for UserViewSet"""

    @classmethod
    def setUpTestData(cls):
        # Create sample user data for testing
        cls.user = cls().get_test_active_regularuser()

    def test_get_user_by_id(self):
        # authenticate the user
        self.client.force_authenticate(user=self.user)
        url = reverse("users:user-list")
        user_id = str(self.user.id)
        response = self.client.get(url, {"by_userId": user_id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer_data = UserSerializer(self.user).data
        self.assertEqual(response.data, serializer_data)

    def test_get_user_by_id_unauthenticated(self):
        url = reverse("users:user-list")
        user_id = str(self.user.id)
        response = self.client.get(url, {"by_userId": user_id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_by_invalid_id_format(self):
        # authenticate the user
        self.client.force_authenticate(user=self.user)
        url = reverse("users:user-list")
        invalid_user_id = "invalid_uuid_format"
        response = self.client.get(url, {"by_userId": invalid_user_id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_user_by_invalid_id_format_unauthenticated(self):
        url = reverse("users:user-list")
        invalid_user_id = "invalid_uuid_format"
        response = self.client.get(url, {"by_userId": invalid_user_id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_user_by_nonexistent_id(self):
        # authenticate the user
        self.client.force_authenticate(user=self.user)
        url = reverse("users:user-list")
        nonexistent_user_id = "550e8400-e29b-41d4-a716-446655440002"
        response = self.client.get(url, {"by_userId": nonexistent_user_id})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user_by_nonexistent_id_unauthenticated(self):
        url = reverse("users:user-list")
        nonexistent_user_id = "550e8400-e29b-41d4-a716-446655440002"
        response = self.client.get(url, {"by_userId": nonexistent_user_id})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_missing_user_id_param(self):
        # authenticate the user
        self.client.force_authenticate(user=self.user)
        url = reverse("users:user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_user_id_param_unauthenticated(self):
        url = reverse("users:user-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
