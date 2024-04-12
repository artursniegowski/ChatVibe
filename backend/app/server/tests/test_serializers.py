from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from server.models import Category, Server
from server.serializers import ChannelSerializer, ServerSerializer, CategorySerializer
from utils.tests.base import BaseTestUser


class CategorySerializerTest(TestCase):
    """Test suit for the CategorySerializer."""
    def setUp(self):
        # Create sample data for testing
        self.category_data = {
            "name": "Test Category",
            "description": "Test Description",
            "icon": SimpleUploadedFile("icon.jpg", b"file_content", content_type="image/jpeg"),
        }

    def test_valid_data(self):
        # Serialize the sample data
        serializer = CategorySerializer(data=self.category_data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)

        # Check that the serialized data matches the input data
        self.assertEqual(serializer.validated_data["name"], self.category_data["name"])
        self.assertEqual(serializer.validated_data["description"], self.category_data["description"])
        self.assertIsNotNone(serializer.validated_data["icon"])

    def test_invalid_data(self):
        # Test with invalid data (missing required field)
        invalid_data = {"description": "This is a test category"}
        serializer = CategorySerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        

class ChannelSerializerTest(TestCase, BaseTestUser):
    @classmethod
    def setUpTestData(cls):
        # Create sample data for testing
        cls.user = cls().get_test_active_regularuser()
        cls.category = Category.objects.create(
            name="Test Category", description="Test Description"
        )
        cls.server = Server.objects.create(
            name="Test server", owner=cls.user, category=cls.category
        )
        cls.channel_data = {
            "name": "Test Channel",
            "topic": "Test Topic",
            "owner": cls.user.id,
            "server": cls.server.id,
        }

    def test_valid_data(self):
        # Serialize the sample data
        serializer = ChannelSerializer(data=self.channel_data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)

        # Check that the serialized data matches the input data
        self.assertEqual(serializer.validated_data["name"], self.channel_data["name"])
        self.assertEqual(serializer.validated_data["topic"], self.channel_data["topic"])
        self.assertEqual(
            serializer.validated_data["owner"].id, self.channel_data["owner"]
        )
        self.assertEqual(
            serializer.validated_data["server"].id, self.channel_data["server"]
        )

    def test_invalid_data(self):
        # Test with invalid data (missing required field)
        invalid_data = {"description": "This is a test channel"}
        serializer = ChannelSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())


class ServerSerializerTest(TestCase, BaseTestUser):
    @classmethod
    def setUpTestData(cls):
        # Create sample data for testing
        cls.user = cls().get_test_active_regularuser()
        cls.category = Category.objects.create(
            name="Test Category", description="Test Description"
        )
        cls.test_server = Server.objects.create(
            name="Test server 2", owner=cls.user, category=cls.category
        )
        cls.channel_data = {  # Define sample channel data
            "name": "Test Channel",
            "topic": "Test Topic",
            "owner": cls.user.id,
            "server": None,  # This will be populated after creating the server
        }
        cls.server_data = {
            "name": "Test server",
            "description": "test serializer desc",
            "owner": cls.user.id,
            "category": cls.category.id,
            "member": [
                cls.user.id,
            ],
            "channel_server": [cls.channel_data],  # Include channel data
        }

    def test_valid_data(self):
        # Serialize the sample data
        server = Server.objects.create(
            name=self.server_data["name"],
            description=self.server_data["description"],
            owner=self.user,
            category=self.category,
        )
        self.channel_data["server"] = server.id

        serializer = ServerSerializer(data=self.server_data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)

        # Check that the serialized data matches the input data
        self.assertEqual(serializer.validated_data["name"], self.server_data["name"])
        self.assertEqual(
            serializer.validated_data["description"], self.server_data["description"]
        )
        self.assertEqual(
            serializer.validated_data["owner"].id, self.server_data["owner"]
        )

    def test_invalid_data(self):
        # Test with invalid data (missing required field)
        invalid_data = {"name": 123}
        serializer = ServerSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())

    def test_category_serialization(self):
        # Test that category gets serilized corectly
        server = Server.objects.create(
            name=self.server_data["name"] + "another",
            description=self.server_data["description"],
            owner=self.user,
            category=self.category,
        )
        serializer = ServerSerializer(server)
        # Assert that the category field is present in the serialized data
        self.assertIn("category", serializer.data)
        # Assert that the value of the category field matches the expected category name
        self.assertEqual(serializer.data["category"], self.category.name)

    def test_to_representation_without_num_members(self):
        # Serialize the test server without num_members
        serializer = ServerSerializer(instance=self.test_server)

        # Check if the serialized data does not contain the num_members field
        serialized_data = serializer.data
        self.assertNotIn("num_members", serialized_data)

    def test_to_representation_with_num_members(self):
        # Set the num_members attribute in the serializer context
        context = {"num_members": True}

        # Serialize the test server with num_members in the context
        serializer = ServerSerializer(instance=self.test_server, context=context)

        # Check if the serialized data contains the num_members field with the correct value
        serialized_data = serializer.data
        self.assertIn("num_members", serialized_data)
