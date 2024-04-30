from django.contrib.auth import get_user_model
from django.test import TestCase

from users.serializers import UserSerializer

User = get_user_model()


class UserSerializerTest(TestCase):
    """Test suite for the UserSerializer."""

    def setUp(self):
        # Create sample user data for testing
        self.user_data = {
            "email": "test@example.com",
            # Add any other fields required for your user model
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
