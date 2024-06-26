from django.conf import settings
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


class LogOutAPIViewTestCase(APITestCase):
    def test_logout(self):
        # Make a POST request to the logout endpoint
        response = self.client.post(reverse("users:logout"))

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert that the refresh and access tokens cookies are cleared
        refresh_token_name = refresh_token_name = getattr(
            settings, "SIMPLE_JWT", {}
        ).get("JWT_AUTH_REFRESH_COOKIE_NAME", "refresh_token")
        access_token_name = self.access_token_name = getattr(
            settings, "SIMPLE_JWT", {}
        ).get("JWT_AUTH_COOKIE_NAME", "access_token")
        self.assertIn(refresh_token_name, response.cookies)
        self.assertIn(access_token_name, response.cookies)
        self.assertEqual(response.cookies[refresh_token_name].value, "")
        self.assertEqual(response.cookies[access_token_name].value, "")
        # Assert that the expiration of the cookies is set to 0
        self.assertEqual(response.cookies[refresh_token_name]["expires"], 0)
        self.assertEqual(response.cookies[access_token_name]["expires"], 0)


class RegisterViewTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse("users:register")

    def test_valid_registration(self):
        data = {"email": "test@example.com", "password": "testpassword"}
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("email" in response.data)

    def test_invalid_registration_missing_field_password(self):
        data = {"email": "test@example.com"}
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_registration_missing_field_email(self):
        data = {"password": "testpassword"}
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_registration_existing_email(self):
        # Create a user with the same email
        User.objects.create_user(email="test@example.com", password="existingpassword")
        data = {"email": "test@example.com", "password": "testpassword"}
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("email" in response.data)

    def test_invalid_email_missing_at(self):
        data = {"email": "testexample.com", "password": "testpassword"}
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("email" in response.data)

    def test_forbidden_email(self):
        data = {"email": "admin@admin.com", "password": "testpassword"}
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
