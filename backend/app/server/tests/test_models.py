import os
from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.utils import DataError, IntegrityError
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

from server.models import Category, Channel, Server
from server.models.category import category_icon_file_path

# from server.models.channel import channel_banner_file_path, channel_icon_file_path
from server.models.server import server_banner_file_path, server_icon_file_path
from utils.tests.base import BaseTestUser

User = get_user_model()


class CategoryModelTestCase(TestCase):
    """Test suit for the Category Model"""

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Category.objects.create(name="Test Category", description="Test Description")
        cls.files_to_clean = []

    def tearDown(self) -> None:
        # cleanig up the files that were created during the tests
        for file_path in self.files_to_clean:
            default_storage.delete(file_path)

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

    @patch("server.models.category.uuid.uuid4")
    def test_category_icon_file_path(self, mocked_uuid: MagicMock):
        # testing if the path is generated corectly
        uuid = "test-uuid"
        mocked_uuid.return_value = uuid
        # Test with a sample file name
        file_name = "home.svg"
        expected_path = os.path.join("uploads", "category", "icon", f"{uuid}.svg")
        file_path = category_icon_file_path(None, file_name)
        self.assertEqual(file_path, expected_path)
        # Test with a file name with multiple dots
        file_name = "file.with.multiple.dots.png"
        expected_path = os.path.join("uploads", "category", "icon", f"{uuid}.png")
        file_path = category_icon_file_path(None, file_name)
        self.assertEqual(file_path, expected_path)
        # Test with an empty file name
        file_name = ""
        with self.assertRaises(ValueError):
            file_path = category_icon_file_path(None, file_name)

    def test_save_method_deletes_existing_icon(self):
        # deleting exisiting icon if it exists
        new_category = Category.objects.create(
            name="Test Category Icon",
            description="Test Description with Icon",
        )
        first_icon = SimpleUploadedFile(
            "new_icon.png", b"file_content", content_type="image/png"
        )
        new_category.icon = first_icon
        new_category.save()

        self.assertTrue(new_category.icon)
        # Ensure the old icon is saved
        first_icon_path = new_category.icon.path
        self.assertTrue(new_category.icon.storage.exists(first_icon_path))

        new_icon = SimpleUploadedFile(
            "new_icon.png", b"file_content", content_type="image/png"
        )
        new_category.icon = new_icon
        new_category.save()

        # Ensure the existing icon is deleted
        self.assertFalse(new_category.icon.storage.exists(first_icon_path))
        # Ensure the new icon is saved
        new_icon_path = new_category.icon.path
        self.assertTrue(new_category.icon.storage.exists(new_icon_path))

        # cleainign the file from media_root
        default_storage.delete(new_icon_path)
        self.assertFalse(new_category.icon.storage.exists(new_icon_path))

    def test_deleting_category_deletes_existing_icon(self):
        """
        Test that deleting category deletes existing icon file
        """
        # saving the icon
        new_category = Category.objects.create(
            name="Test Category Icon - to delete",
            description="Test Description with Icon to delte",
        )
        icon_file = SimpleUploadedFile(
            "new_icon_to_delete.png", b"file_content", content_type="image/png"
        )
        new_category.icon = icon_file
        new_category.save()
        # checking if the icon exists
        new_icon_path = new_category.icon.path
        self.assertTrue(new_category.icon.storage.exists(new_icon_path))
        # deleting the category
        new_category.delete()
        # checking if the icon got deleted too.
        self.assertFalse(new_category.icon.storage.exists(new_icon_path))

    def test_category_creation_with_invalid_icon_image_size(self):
        # crate icon that size is bigger than the allowed size
        content = b"X" * 251 * 1024  # 251KB
        icon_file = SimpleUploadedFile("banner.svg", content, content_type="text/plain")

        # Attempt to create a Category instance with invalid image size
        category = Category.objects.create(
            name="Test Category invalid file size",
            description="Test Description invalid file size",
            # Upload icon images with invalid size
            icon=icon_file,
        )
        # file to be cleaned at the end of all tests
        icon_file_path = category.icon.path
        self.files_to_clean.append(icon_file_path)

        # print(Category._meta.get_field("icon").validators[0].max_file_size)
        with self.assertRaises(ValidationError) as context:
            category.full_clean()

        error_dict = context.exception.error_dict

        self.assertIn("icon", error_dict)
        self.assertEqual(len(error_dict["icon"]), 1)

    def test_category_creation_with_valid_icon_image_size(self):
        # crate icon that size is within the limit of the allowed size
        content = b"X" * 250 * 1024  # 250KB
        icon_file = SimpleUploadedFile("banner.svg", content, content_type="text/plain")

        # Attempt to create a Category instance with invalid image size
        category = Category.objects.create(
            name="Test Category invalid file size",
            description="Test Description invalid file size",
            # Upload icon images with invalid size
            icon=icon_file,
        )
        # file to be cleaned at the end of all tests
        icon_file_path = category.icon.path
        self.files_to_clean.append(icon_file_path)

        self.assertTrue(category)
        try:
            category.full_clean()
        except Exception as e:
            exception_name = type(e).__name__
            print(f"Exception raised: {exception_name}")
            self.fail(
                "test_category_creation_with_valid_icon_image_size() \
                raised Exception: {exception_name} unexpectedly!"
            )


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
        cls.files_to_clean = []

    def tearDown(self) -> None:
        # cleanig up the files that were created during the tests
        for file_path in self.files_to_clean:
            default_storage.delete(file_path)

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
        cls.files_to_clean = []

    def tearDown(self) -> None:
        # cleanig up the files that were created during the tests
        for file_path in self.files_to_clean:
            default_storage.delete(file_path)

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

    @patch("server.models.server.uuid.uuid4")
    def test_server_icon_file_path(self, mocked_uuid: MagicMock):
        # test if the path is generated corectly
        uuid = "test-uuid-server"
        mocked_uuid.return_value = uuid
        # Test with a sample file name
        file_name = "home.svg"
        expected_path = os.path.join("uploads", "server", "icon", f"{uuid}.svg")
        file_path = server_icon_file_path(None, file_name)
        self.assertEqual(file_path, expected_path)
        # Test with a file name with multiple dots
        file_name = "file.with.multiple.dots.png"
        expected_path = os.path.join("uploads", "server", "icon", f"{uuid}.png")
        file_path = server_icon_file_path(None, file_name)
        self.assertEqual(file_path, expected_path)
        # Test with an empty file name
        file_name = ""
        with self.assertRaises(ValueError):
            file_path = server_icon_file_path(None, file_name)

    @patch("server.models.server.uuid.uuid4")
    def test_server_banner_file_path(self, mocked_uuid: MagicMock):
        # test if the path is generated corectly
        uuid = "test-uuid-server"
        mocked_uuid.return_value = uuid
        # Test with a sample file name
        file_name = "home.svg"
        expected_path = os.path.join("uploads", "server", "banner", f"{uuid}.svg")
        file_path = server_banner_file_path(None, file_name)
        self.assertEqual(file_path, expected_path)
        # Test with a file name with multiple dots
        file_name = "file.with.multiple.dots.png"
        expected_path = os.path.join("uploads", "server", "banner", f"{uuid}.png")
        file_path = server_banner_file_path(None, file_name)
        self.assertEqual(file_path, expected_path)
        # Test with an empty file name
        file_name = ""
        with self.assertRaises(ValueError):
            file_path = server_banner_file_path(None, file_name)

    def test_save_method_deletes_existing_icon(self):
        # deleting exisiting icon if it exists
        server_test = Server.objects.create(
            name="test-ser",
            description="test description",
            owner=self.user,
            category=self.category,
        )
        icon_first = SimpleUploadedFile(
            "new_icon.png", b"file_content", content_type="image/png"
        )
        # checking if the icon is empty
        self.assertFalse(server_test.icon)
        # saving first icon
        server_test.icon = icon_first
        server_test.save()

        # checks if the icon was saved and stored
        icon_first_path = server_test.icon.path
        self.files_to_clean.append(icon_first_path)
        self.assertTrue(server_test.icon)
        self.assertTrue(server_test.icon.storage.exists(icon_first_path))

        # saving a new icon
        new_icon = SimpleUploadedFile(
            "new_icon_2.png", b"file_content", content_type="image/png"
        )
        server_test.icon = new_icon
        server_test.save()
        icon_new_path = server_test.icon.path
        self.files_to_clean.append(icon_new_path)
        self.assertTrue(server_test.icon)
        self.assertTrue(server_test.icon.storage.exists(icon_new_path))

        # Ensure the first icon was deleted
        self.assertFalse(server_test.icon.storage.exists(icon_first_path))

        # cleainign the file from media_root
        default_storage.delete(icon_new_path)
        self.assertFalse(server_test.icon.storage.exists(icon_new_path))

    def test_save_method_deletes_existing_banner(self):
        # deleting exisiting banner if it exists
        server_test = Server.objects.create(
            name="test-ser",
            description="test description",
            owner=self.user,
            category=self.category,
        )
        banner_first = SimpleUploadedFile(
            "new_banner.png", b"file_content", content_type="image/png"
        )
        # checking if the banner is empty
        self.assertFalse(server_test.banner)
        # saving first banner
        server_test.banner = banner_first
        server_test.save()

        # checks if the banner was saved and stored
        banner_first_path = server_test.banner.path
        self.files_to_clean.append(banner_first_path)
        self.assertTrue(server_test.banner)
        self.assertTrue(server_test.banner.storage.exists(banner_first_path))

        # saving a new banner
        banner_icon = SimpleUploadedFile(
            "new_banner_2.png", b"file_content", content_type="image/png"
        )
        server_test.banner = banner_icon
        server_test.save()
        banner_new_path = server_test.banner.path
        self.files_to_clean.append(banner_new_path)
        self.assertTrue(server_test.banner)
        self.assertTrue(server_test.banner.storage.exists(banner_new_path))

        # Ensure the first banner was deleted
        self.assertFalse(server_test.banner.storage.exists(banner_first_path))

        # cleainign the file from media_root
        default_storage.delete(banner_new_path)
        self.assertFalse(server_test.banner.storage.exists(banner_new_path))

    def test_deleting_server_deletes_existing_icon(self):
        """
        Test that deleting server deletes existing icon file
        """
        # saving the icon
        server_test = Server.objects.create(
            name="test-ser",
            description="test description",
            owner=self.user,
            category=self.category,
        )
        icon_file = SimpleUploadedFile(
            "new_icon_to_delete.png", b"file_content", content_type="image/png"
        )
        self.assertFalse(server_test.icon)
        server_test.icon = icon_file
        server_test.save()
        # checking if the icon exists
        icon_path = server_test.icon.path
        self.files_to_clean.append(icon_path)
        self.assertTrue(server_test.icon)
        self.assertTrue(server_test.icon.storage.exists(icon_path))
        # deleting the channel
        server_test.delete()
        # checking if the icon got deleted too.
        self.assertFalse(server_test.icon.storage.exists(icon_path))

    def test_deleting_server_deletes_existing_banner(self):
        """
        Test that deleting server deletes existing banner file
        """
        # saving the icon
        server_test = Server.objects.create(
            name="test-ser",
            description="test description",
            owner=self.user,
            category=self.category,
        )
        icon_file = SimpleUploadedFile(
            "new_banner_to_delete.png", b"file_content", content_type="image/png"
        )
        self.assertFalse(server_test.banner)
        server_test.banner = icon_file
        server_test.save()
        # checking if the banner exists
        banner_path = server_test.banner.path
        self.files_to_clean.append(banner_path)
        self.assertTrue(server_test.banner)
        self.assertTrue(server_test.banner.storage.exists(banner_path))
        # deleting the channel
        server_test.delete()
        # checking if the icon got deleted too.
        self.assertFalse(server_test.banner.storage.exists(banner_path))

    @patch("server.validators.image_file_size.Image.open")
    def test_server_creation_with_invalid_icon_image_extensions(
        self, mocked_open: MagicMock
    ):
        # Attempt to create a server instance with invalid image extensions
        server_test = Server.objects.create(
            name="test-ser",
            description="test description",
            owner=self.user,
            category=self.category,
            icon=SimpleUploadedFile("icon.txt", b"content", content_type="text/plain"),
        )

        # file to be cleaned at the end of all tests
        icon_file_path = server_test.icon.path
        self.files_to_clean.append(icon_file_path)
        mocked_img = MagicMock()
        mocked_img.size = (30, 30)  # Mock image size
        mocked_open.return_value.__enter__.return_value = (
            mocked_img  # Simulate context manager
        )

        with self.assertRaises(ValidationError) as context:
            server_test.full_clean()

        error_dict = context.exception.error_dict

        self.assertIn("icon", error_dict)
        self.assertEqual(len(error_dict["icon"]), 1)

        # not neede as it is taken care by the tearDown method
        # if channel:
        #     # make sure the file gets delted after it gets created
        #     icon_path = channel.icon.path
        #     channel.delete()
        #     self.assertFalse(channel.icon.storage.exists(icon_path))

        #     # self.files_to_clean.pop()
        #     self.files_to_clean.remove(icon_file_path)

    @patch("server.validators.image_file_size.Image.open")
    def test_server_creation_with_valid_icon_image_extensions(
        self, mocked_open: MagicMock
    ):
        # Attempt to create a server instance with valid image extensions
        server_test = Server.objects.create(
            name="test-ser",
            description="test description",
            owner=self.user,
            category=self.category,
            icon=SimpleUploadedFile("icon.png", b"content", content_type="text/plain"),
        )

        # file to be cleaned at the end of all tests
        icon_file_path = server_test.icon.path
        self.files_to_clean.append(icon_file_path)
        mocked_img = MagicMock()
        mocked_img.size = (30, 30)  # Mock image size
        mocked_open.return_value.__enter__.return_value = (
            mocked_img  # Simulate context manager
        )

        self.assertTrue(server_test)
        try:
            server_test.full_clean()
        except Exception as e:
            exception_name = type(e).__name__
            print(f"Exception raised: {exception_name}")
            self.fail(
                "test_server_creation_with_valid_icon_image_extensions() \
                raised Exception: {exception_name} unexpectedly!"
            )

    @patch("server.validators.image_file_size.Image.open")
    def test_server_creation_with_invalid_banner_image_extensions(
        self, mocked_open: MagicMock
    ):
        # Attempt to create a server instance with invalid image extensions
        server_test = Server.objects.create(
            name="test-ser",
            description="test description",
            owner=self.user,
            category=self.category,
            banner=SimpleUploadedFile(
                "banner.txt", b"content", content_type="text/plain"
            ),
        )

        # file to be cleaned at the end of all tests
        banner_file_path = server_test.banner.path
        self.files_to_clean.append(banner_file_path)
        mocked_img = MagicMock()
        mocked_img.size = (30, 30)  # Mock image size
        mocked_open.return_value.__enter__.return_value = (
            mocked_img  # Simulate context manager
        )

        with self.assertRaises(ValidationError) as context:
            server_test.full_clean()

        error_dict = context.exception.error_dict

        self.assertIn("banner", error_dict)
        self.assertEqual(len(error_dict["banner"]), 1)

        # not neede as it is taken care by the tearDown method
        # if channel:
        #     # make sure the file gets delted after it gets created
        #     banner_path = channel.icon.path
        #     channel.delete()
        #     self.assertFalse(channel.icon.storage.exists(banner_path))

        #     # self.files_to_clean.pop()
        #     self.files_to_clean.remove(banner_file_path)

    @patch("server.validators.image_file_size.Image.open")
    def test_server_creation_with_valid_banner_image_extensions(
        self, mocked_open: MagicMock
    ):
        # Attempt to create a server instance with valid image extensions
        server_test = Server.objects.create(
            name="test-ser",
            description="test description",
            owner=self.user,
            category=self.category,
            # Upload banner and icon images with invalid extensions
            banner=SimpleUploadedFile(
                "banner.png", b"content", content_type="text/plain"
            ),
        )
        # file to be cleaned at the end of all tests
        banner_file_path = server_test.banner.path
        self.files_to_clean.append(banner_file_path)
        mocked_img = MagicMock()
        mocked_img.size = (30, 30)  # Mock image size
        mocked_open.return_value.__enter__.return_value = (
            mocked_img  # Simulate context manager
        )

        self.assertTrue(server_test)
        try:
            server_test.full_clean()
        except Exception as e:
            exception_name = type(e).__name__
            print(f"Exception raised: {exception_name}")
            self.fail(
                "test_server_creation_with_valid_banner_image_extensions() \
                raised Exception: {exception_name} unexpectedly!"
            )

    @patch("server.validators.image_file_size.Image.open")
    def test_server_creation_with_invalid_banner_image_size_width(
        self, mocked_open: MagicMock
    ):
        # Attempt to create a Server instance with invalid image size width
        server_test = Server.objects.create(
            name="test-ser",
            description="test description",
            owner=self.user,
            category=self.category,
            # Upload banner and icon images with invalid extensions
            banner=SimpleUploadedFile(
                "banner.png", b"content", content_type="text/plain"
            ),
        )

        # file to be cleaned at the end of all tests
        banner_file_path = server_test.banner.path
        self.files_to_clean.append(banner_file_path)
        mocked_img = MagicMock()
        mocked_img.size = (3001, 3000)  # Mock image size
        mocked_open.return_value.__enter__.return_value = (
            mocked_img  # Simulate context manager
        )

        with self.assertRaises(ValidationError) as context:
            server_test.full_clean()

        error_dict = context.exception.error_dict

        self.assertIn("banner", error_dict)
        self.assertEqual(len(error_dict["banner"]), 1)

    @patch("server.validators.image_file_size.Image.open")
    def test_server_creation_with_invalid_banner_image_size_height(
        self, mocked_open: MagicMock
    ):
        # Attempt to create a Server instance with invalid image size height
        server_test = Server.objects.create(
            name="test-ser",
            description="test description",
            owner=self.user,
            category=self.category,
            # Upload banner and icon images with invalid extensions
            banner=SimpleUploadedFile(
                "banner.png", b"content", content_type="text/plain"
            ),
        )
        # file to be cleaned at the end of all tests
        banner_file_path = server_test.banner.path
        self.files_to_clean.append(banner_file_path)
        mocked_img = MagicMock()
        mocked_img.size = (3000, 3001)  # Mock image size
        mocked_open.return_value.__enter__.return_value = (
            mocked_img  # Simulate context manager
        )

        with self.assertRaises(ValidationError) as context:
            server_test.full_clean()

        error_dict = context.exception.error_dict

        self.assertIn("banner", error_dict)
        self.assertEqual(len(error_dict["banner"]), 1)

    @patch("server.validators.image_file_size.Image.open")
    def test_server_creation_with_valid_banner_image_size(self, mocked_open: MagicMock):
        # Attempt to create a Server instance with valid image size
        server_test = Server.objects.create(
            name="test-ser",
            description="test description",
            owner=self.user,
            category=self.category,
            # Upload banner and icon images with invalid extensions
            banner=SimpleUploadedFile(
                "banner.png", b"content", content_type="text/plain"
            ),
        )
        # file to be cleaned at the end of all tests
        banner_file_path = server_test.banner.path
        self.files_to_clean.append(banner_file_path)
        mocked_img = MagicMock()
        mocked_img.size = (3000, 3000)  # Mock image size
        mocked_open.return_value.__enter__.return_value = (
            mocked_img  # Simulate context manager
        )

        self.assertTrue(server_test)
        try:
            server_test.full_clean()
        except Exception as e:
            exception_name = type(e).__name__
            print(f"Exception raised: {exception_name}")
            self.fail(
                "test_server_creation_with_valid_banner_image_size() \
                raised Exception: {exception_name} unexpectedly!"
            )

    @patch("server.validators.image_file_size.Image.open")
    def test_server_creation_with_invalid_icon_image_size_width(
        self, mocked_open: MagicMock
    ):
        # Attempt to create a Channel instance with invalid image size width
        server_test = Server.objects.create(
            name="test-ser",
            description="test description",
            owner=self.user,
            category=self.category,
            # Upload banner and icon images with invalid extensions
            icon=SimpleUploadedFile("icon.png", b"content", content_type="text/plain"),
        )

        # file to be cleaned at the end of all tests
        icon_file_path = server_test.icon.path
        self.files_to_clean.append(icon_file_path)
        mocked_img = MagicMock()
        mocked_img.size = (71, 70)  # Mock image size
        mocked_open.return_value.__enter__.return_value = (
            mocked_img  # Simulate context manager
        )

        with self.assertRaises(ValidationError) as context:
            server_test.full_clean()

        error_dict = context.exception.error_dict

        self.assertIn("icon", error_dict)
        self.assertEqual(len(error_dict["icon"]), 1)

    @patch("server.validators.image_file_size.Image.open")
    def test_server_creation_with_invalid_icon_image_size_height(
        self, mocked_open: MagicMock
    ):
        # Attempt to create a Sever instance with invalid image size height
        server_test = Server.objects.create(
            name="test-ser",
            description="test description",
            owner=self.user,
            category=self.category,
            # Upload banner and icon images with invalid extensions
            icon=SimpleUploadedFile("icon.png", b"content", content_type="text/plain"),
        )
        # file to be cleaned at the end of all tests
        icon_file_path = server_test.icon.path
        self.files_to_clean.append(icon_file_path)
        mocked_img = MagicMock()
        mocked_img.size = (70, 71)  # Mock image size
        mocked_open.return_value.__enter__.return_value = (
            mocked_img  # Simulate context manager
        )

        with self.assertRaises(ValidationError) as context:
            server_test.full_clean()

        error_dict = context.exception.error_dict

        self.assertIn("icon", error_dict)
        self.assertEqual(len(error_dict["icon"]), 1)

    @patch("server.validators.image_file_size.Image.open")
    def test_server_creation_with_valid_icon_image_size(self, mocked_open: MagicMock):
        # Attempt to create a Server instance with valid image size
        server_test = Server.objects.create(
            name="test-ser",
            description="test description",
            owner=self.user,
            category=self.category,
            # Upload banner and icon images with invalid extensions
            icon=SimpleUploadedFile("icon.png", b"content", content_type="text/plain"),
        )
        # file to be cleaned at the end of all tests
        icon_file_path = server_test.icon.path
        self.files_to_clean.append(icon_file_path)
        mocked_img = MagicMock()
        mocked_img.size = (70, 70)  # Mock image size
        mocked_open.return_value.__enter__.return_value = (
            mocked_img  # Simulate context manager
        )

        self.assertTrue(server_test)
        try:
            server_test.full_clean()
        except Exception as e:
            exception_name = type(e).__name__
            print(f"Exception raised: {exception_name}")
            self.fail(
                "test_server_creation_with_valid_icon_image_size() \
                raised Exception: {exception_name} unexpectedly!"
            )

        # refering to the values of the validator
        # print(
        #     Channel._meta.get_field("banner").validators[0].max_width,
        #     Channel._meta.get_field("banner").validators[0].max_height,
        # )
