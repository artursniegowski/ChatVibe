from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from PIL import Image


@deconstructible
class ImageSizeValidator:
    """
    Validator to ensure that an uploaded image does not exceed a specified maximum size.

    Attributes:
        max_width (int): The maximum allowed width of the image in pixels.
        max_height (int): The maximum allowed height of the image in pixels.
        message (str): The error message to be raised if the image dimensions exceed the maximum allowed size.
            It can contain placeholders such as %(allowed_width)s and %(allowed_height)s for the maximum allowed
            width and height, and %(image_width)s and %(image_height)s for the actual width and height of the image.
        code (str): An optional error code to identify the type of validation error.

    Methods:
        __init__: Initializes the validator with the specified parameters.
        __call__: Validates the dimensions of the input image against the maximum allowed size.
        __eq__: Compares two instances of ImageSizeValidator for equality based on their attributes.

    Example:
        To use this validator in a model's ImageField:

        ```
        from django.core.exceptions import ValidationError
        from django.db import models
        from myapp.validators import ImageSizeValidator

        class MyModel(models.Model):
            image = models.ImageField(
                upload_to='images/',
                validators=[ImageSizeValidator(max_width=100, max_height=100)]
            )
        ```
    """

    max_width = 70  # in pixels
    max_height = 70
    message = _(
        "The image dimensions exceed the maximum allowed size %(allowed_width)s x %(allowed_height)s.\
            The image size was %(image_width)s x %(image_height)s."
    )
    code = "image_size_exceeded"

    def __init__(self, max_width=None, max_height=None, message=None, code=None):
        if max_width is not None:
            self.max_width = max_width
        if max_height is not None:
            self.max_height = max_height
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, image: UploadedFile) -> None:
        """
        Validate that the input image is not greater than the given size in pixels
        """
        if image:
            with Image.open(image) as img:
                width, height = img.size
                if width > self.max_width or height > self.max_height:
                    params = {
                        "image_width": width,
                        "image_height": height,
                        "allowed_width": self.max_width,
                        "allowed_height": self.max_height,
                    }
                    raise ValidationError(self.message, code=self.code, params=params)

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, ImageSizeValidator)
            and (self.max_width == other.max_width)
            and (self.max_height == other.max_height)
            and (self.message == other.message)
            and (self.code == other.code)
        )
