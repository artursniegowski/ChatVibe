from unittest.mock import MagicMock, patch

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase

from server.validators import (
    FileSizeValidator,
    ImageSizeValidator,
    validate_image_file_extension,
)
from server.validators.image_file_extensions import VALID_IMAGE_EXTENSIONS


class ImageFileExtensionValidatorTests(SimpleTestCase):
    """
    Test suit for validate_image_file_extension validator
    """

    def test_valid_image_file_extension(self):
        # Test with valid image extensions
        for ext in VALID_IMAGE_EXTENSIONS:
            file_name = f"test_image{ext}"
            file_content = b"dummy content"
            uploaded_file = SimpleUploadedFile(file_name, file_content)
            try:
                validate_image_file_extension(uploaded_file)
            except ValidationError:
                self.fail(
                    f"validate_image_file_extension raised ValidationError for valid extension {ext}"
                )

    def test_invalid_image_file_extension(self):
        # Test with invalid image extensions
        invalid_extensions = [
            ".txt",
            ".pdf",
            ".docx",
            ".doc",
            ".svg",
            ".js",
            ".7z",
            ".csv",
            ".dat",
            ".apk",
            ".exe",
            ".bin",
        ]
        for ext in invalid_extensions:
            file_name = f"test_image{ext}"
            file_content = b"dummy content"
            uploaded_file = SimpleUploadedFile(file_name, file_content)
            with self.assertRaises(ValidationError):
                validate_image_file_extension(uploaded_file)


class FileSizeValidatorTests(SimpleTestCase):
    """
    Test suit for the FileSizeValidator
    """

    def test_file_size_validator_default_values_kb(self):
        validator = FileSizeValidator()
        self.assertEqual(validator.max_file_size, 500)
        self.assertFalse(validator.size_in_mb)
        self.assertEqual(validator.code, "file_size_exceeded")

    def test_file_size_validator_custom_values_mb(self):
        validator = FileSizeValidator(max_file_size=2, size_in_mb=True)
        self.assertEqual(validator.max_file_size, 2)
        self.assertTrue(validator.size_in_mb)

    def test_file_size_validator_custom_message_and_code(self):
        custom_message = "Custom message"
        custom_code = "custom_code"
        validator = FileSizeValidator(message=custom_message, code=custom_code)
        self.assertEqual(validator.message, custom_message)
        self.assertEqual(validator.code, custom_code)

    def test_file_size_validator_call_within_allowed_size_kb(self):
        validator = FileSizeValidator(max_file_size=1)  # 1KB
        mocked_file = MagicMock(size=1024)  # 1KB
        validator(mocked_file)  # Should not raise ValidationError

    def test_file_size_validator_call_within_allowed_size_mb(self):
        validator = FileSizeValidator(max_file_size=1, size_in_mb=True)  # 1MB
        mocked_file = MagicMock(size=1048576)  # 1MB
        validator(mocked_file)  # Should not raise ValidationError

    def test_file_size_validator_call_exceeds_allowed_size_kb(self):
        validator = FileSizeValidator(max_file_size=1)  # 1KB
        mocked_file = MagicMock(size=2048)  # 2KB
        with self.assertRaises(ValidationError):
            validator(mocked_file)

    def test_file_size_validator_call_exceeds_allowed_size_mb(self):
        validator = FileSizeValidator(max_file_size=1, size_in_mb=True)  # 1MB
        mocked_file = MagicMock(size=2097152)  # 2MB
        with self.assertRaises(ValidationError):
            validator(mocked_file)

    def test_file_size_validator_comparison(self):
        validator1 = FileSizeValidator(max_file_size=1, size_in_mb=True)
        validator2 = FileSizeValidator(max_file_size=1, size_in_mb=True)
        validator3 = FileSizeValidator(max_file_size=2, size_in_mb=True)
        self.assertEqual(validator1, validator2)
        self.assertNotEqual(validator1, validator3)


class ImageSizeValidatorTests(SimpleTestCase):
    """
    Test suit for ImageSizeValidator
    """

    def test_image_size_validator_default_values(self):
        validator = ImageSizeValidator()
        self.assertEqual(validator.max_width, 70)
        self.assertEqual(validator.max_height, 70)

    def test_image_size_validator_custom_values(self):
        validator = ImageSizeValidator(max_width=100, max_height=80)
        self.assertEqual(validator.max_width, 100)
        self.assertEqual(validator.max_height, 80)

    def test_image_size_validator_custom_message_and_code(self):
        custom_message = "Custom message"
        custom_code = "custom_code"
        validator = ImageSizeValidator(message=custom_message, code=custom_code)
        self.assertEqual(validator.message, custom_message)
        self.assertEqual(validator.code, custom_code)

    @patch("server.validators.image_file_size.Image.open")
    def test_image_size_validator_call_within_allowed_size(
        self, mocked_open: MagicMock
    ):
        validator = ImageSizeValidator(max_width=100, max_height=80)
        mocked_img = MagicMock()
        mocked_img.size = (90, 70)  # Mock image size
        mocked_open.return_value.__enter__.return_value = (
            mocked_img  # Simulate context manager
        )
        mocked_file = MagicMock()
        validator(mocked_file)  # Should not raise ValidationError

    @patch("server.validators.image_file_size.Image.open")
    def test_image_size_validator_call_exceeds_allowed_width(
        self, mocked_open: MagicMock
    ):
        validator = ImageSizeValidator(max_width=100, max_height=80)
        mocked_img = MagicMock()
        mocked_img.size = (110, 70)  # Mock image size exceeding max width
        mocked_open.return_value.__enter__.return_value = (
            mocked_img  # Simulate context manager
        )
        mocked_file = MagicMock()
        with self.assertRaises(ValidationError):
            validator(mocked_file)

    @patch("server.validators.image_file_size.Image.open")
    def test_image_size_validator_call_exceeds_allowed_height(
        self, mocked_open: MagicMock
    ):
        validator = ImageSizeValidator(max_width=100, max_height=80)
        mocked_img = MagicMock()
        mocked_img.size = (90, 90)  # Mock image size exceeding max height
        mocked_open.return_value.__enter__.return_value = (
            mocked_img  # Simulate context manager
        )
        mocked_file = MagicMock()
        with self.assertRaises(ValidationError):
            validator(mocked_file)

    def test_image_size_validator_comparison(self):
        validator1 = ImageSizeValidator(max_width=100, max_height=80)
        validator2 = ImageSizeValidator(max_width=100, max_height=80)
        validator3 = ImageSizeValidator(max_width=200, max_height=80)
        self.assertEqual(validator1, validator2)
        self.assertNotEqual(validator1, validator3)
