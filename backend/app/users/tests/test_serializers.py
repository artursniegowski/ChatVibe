from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import serializers

from users.serializers import RegisterSerializer, UserSerializer

User = get_user_model()


class UserSerializerTest(TestCase):
    """Test suite for the UserSerializer."""

    def setUp(self):
        # Create sample user data for testing
        self.user_data = {
            "email": "test@example.com",
        }

    def test_valid_data(self):
        # Serialize the sample user data
        serializer = UserSerializer(data=self.user_data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)

        # Check that the serialized data matches the input data
        self.assertEqual(serializer.validated_data["email"], self.user_data["email"])

    def test_invalid_data(self):
        # Test with invalid data (missing required field)
        invalid_data = {}  # Missing required 'email' field
        serializer = UserSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())


class RegisterSerializerTest(TestCase):
    """Test suite for the RegisterSerializer."""

    def setUp(self):
        # Create sample user data for testing
        self.user_data = {
            "email": "test@example.com",
            "password": "any-password-test!!",
        }

    def test_valid_data(self):
        # Serialize the sample user data
        serializer = RegisterSerializer(data=self.user_data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)

        # Check that the serialized data matches the input data
        self.assertEqual(serializer.validated_data["email"], self.user_data["email"])
        self.assertEqual(
            serializer.validated_data["password"], self.user_data["password"]
        )

    def test_invalid_data_empty_data(self):
        # Test with invalid data (missing required field)
        invalid_data = {}  # Missing required 'email' field
        serializer = RegisterSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_invalid_data_wrong_email_format_missing_at(self):
        # Test password validation (e.g., minimum length)
        invalid_password_data = {"email": "testexample.com", "password": "anypassword"}
        serializer = RegisterSerializer(data=invalid_password_data)
        self.assertFalse(serializer.is_valid())

    def test_invalid_data_wrong_email_format_missing_dot_end(self):
        # Test password validation (e.g., minimum length)
        invalid_password_data = {"email": "test@example", "password": "anypassword"}
        serializer = RegisterSerializer(data=invalid_password_data)
        self.assertFalse(serializer.is_valid())

    def test_invalid_data_missing_password(self):
        # Test password validation (e.g., minimum length)
        invalid_password_data = {"email": "test@example", "password": ""}
        serializer = RegisterSerializer(data=invalid_password_data)
        self.assertFalse(serializer.is_valid())

    def test_unique_email_constraint(self):
        # Test unique email constraint
        User.objects.create_user(
            email=self.user_data["email"], password="existing-password"
        )
        serializer = RegisterSerializer(data=self.user_data)
        with self.assertRaises(serializers.ValidationError):
            serializer.is_valid(raise_exception=True)
        self.assertIn("email", serializer.errors)
        self.assertEqual(serializer.errors["email"][0].code, "unique")

    def test_create_method(self):
        # Test create method
        serializer = RegisterSerializer(data=self.user_data)
        serializer.is_valid()
        user = serializer.save()
        self.assertEqual(user.email, self.user_data["email"])
        # Query the database to check if the user was created
        created_user = User.objects.get(email=self.user_data["email"])
        self.assertEqual(created_user.email, self.user_data["email"])

    def test_extra_kwargs_password_write_only(self):
        serializer = RegisterSerializer()
        self.assertTrue(serializer.fields["password"].write_only)
