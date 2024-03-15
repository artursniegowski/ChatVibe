from django.contrib.auth import get_user_model
from django.db.utils import DataError, IntegrityError
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from server.models import Category, Channel, Server
from utils.tests.base import BaseTestUser

User = get_user_model()


class CategoryModelTestCase(TestCase):
    """Test suit for the Category Model"""

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Category.objects.create(name="Test Category", description="Test Description")

    def test_verbose_name_plural(self):
        self.assertEqual(str(Category._meta.verbose_name_plural), _("Categories"))

    def test_string_representation(self):
        category = Category.objects.first()
        self.assertEqual(str(category), category.name)

    def test_name_is_required_fail(self):
        # Attempt to create a Category without a name
        with self.assertRaises(ValueError):
            Category.objects.create()

    def test_creating_a_category_only_with_name(self):
        # Attempt to create a Category only with a name
        category = Category.objects.create(name="another test")
        category_exists = Category.objects.filter(name=category.name).exists()
        self.assertTrue(category_exists)

    def test_max_length_name(self):
        # Attempt to create a Category with a name longer than 100 characters
        max_length = Category._meta.get_field("name").max_length
        long_name = "a" * (max_length + 1)
        with self.assertRaises(DataError):
            Category.objects.create(name=long_name)

    def test_max_length_description(self):
        # Attempt to create a Category with a description longer than 300 characters
        max_length = Category._meta.get_field("description").max_length
        name = "any"
        description = "d" * (max_length + 1)
        with self.assertRaises(DataError):
            Category.objects.create(name=name, description=description)

    def test_name_uniqueness(self):
        # Create a Category with a specific name
        category_name = "Test Category"

        # Attempt to create another Category with the same name
        with self.assertRaises(IntegrityError):
            Category.objects.create(name=category_name)


class ChannelModelTestCase(TestCase, BaseTestUser):
    """Test suit for the Category Model"""

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = cls().get_test_active_regularuser()
        cls.category = Category.objects.create(
            name="Test Category", description="Test Description"
        )

        cls.server = Server.objects.create(
            name="Test server", owner=cls.user, category=cls.category
        )
        cls.channel = Channel.objects.create(
            name="First Channel", owner=cls.user, server=cls.server
        )

    def test_name_max_length_fail(self):
        # Test max length for name field
        max_length = Channel._meta.get_field("name").max_length
        with self.assertRaises(DataError):
            Channel.objects.create(
                name="a" * (max_length + 1),
                owner=self.user,
                topic="Test Topic",
                server=self.server,
            )

    def test_name_max_length_success(self):
        # Test max length for name field
        max_length = Channel._meta.get_field("name").max_length
        channel = Channel.objects.create(
            name="a" * max_length,
            owner=self.user,
            topic="Test Topic",
            server=self.server,
        )
        self.assertEqual(len(channel.name), max_length)

    def test_name_strip_and_lower(self):
        # Test if name is stripped and lowercased
        channel = Channel.objects.create(
            name=" Test Channel ",
            owner=self.user,
            topic="Test Topic",
            server=self.server,
        )
        self.assertEqual(channel.name, "test channel")

    def test_topic_max_length_success(self):
        # Test max length for topic field
        max_length = Channel._meta.get_field("topic").max_length
        channel = Channel.objects.create(
            name="Test Channel",
            owner=self.user,
            topic="a" * max_length,
            server=self.server,
        )
        self.assertEqual(len(channel.topic), max_length)

    def test_topic_max_length_fail(self):
        # Test max length for topic field
        max_length = Channel._meta.get_field("topic").max_length
        with self.assertRaises(DataError):
            Channel.objects.create(
                name="Test Channel",
                owner=self.user,
                topic="a" * (max_length + 1),
                server=self.server,
            )

    def test_owner_relationship(self):
        # Test owner relationship
        self.assertEqual(self.channel.owner, self.user)

    def test_server_relationship(self):
        # Test server relationship
        self.assertEqual(self.channel.server, self.server)

    def test_string_representation(self):
        # testing the string representation
        self.assertEqual(str(self.channel), self.channel.name)


class ServerModelTestCase(TestCase, BaseTestUser):
    """Test suit for the Category Model"""

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = cls().get_test_active_regularuser()
        cls.category = Category.objects.create(
            name="Test Category", description="Test Description"
        )

        cls.server = Server.objects.create(
            name="Test server", owner=cls.user, category=cls.category
        )

    def test_string_representation(self):
        # testing the string representation
        self.assertEqual(str(self.server), self.server.name)

    def test_name_max_length_fail(self):
        # Test max length for name field
        max_length = Server._meta.get_field("name").max_length
        with self.assertRaises(DataError):
            Server.objects.create(
                name="a" * (max_length + 1), owner=self.user, category=self.category
            )

    def test_name_max_length_success(self):
        # Test max length for name field
        max_length = Server._meta.get_field("name").max_length
        server = Server.objects.create(
            name="a" * max_length, owner=self.user, category=self.category
        )
        self.assertEqual(len(server.name), max_length)

    def test_description_max_length_fail(self):
        # Test max length for name field
        max_length = Server._meta.get_field("description").max_length
        with self.assertRaises(DataError):
            Server.objects.create(
                name="test-ser",
                description="a" * (max_length + 1),
                owner=self.user,
                category=self.category,
            )

    def test_description_max_length_success(self):
        # Test max length for name field
        max_length = Server._meta.get_field("description").max_length
        server = Server.objects.create(
            name="test-ser",
            description="a" * max_length,
            owner=self.user,
            category=self.category,
        )
        self.assertEqual(len(server.description), max_length)

    def test_owner_relationship(self):
        # Test owner relationship
        self.assertEqual(self.server.owner, self.user)

    def test_category_relationship(self):
        # Test owner relationship
        self.assertEqual(self.server.category, self.category)
