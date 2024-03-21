import os

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

# valid extensions
VALID_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}


def validate_image_file_extension(value: UploadedFile) -> None:
    """
    Checking if the extensions of the file is in format of VALID_IMAGE_EXTENSIONS
    """
    ext = os.path.splitext(value.name)[1]
    if not ext.lower() in VALID_IMAGE_EXTENSIONS:
        raise ValidationError("Unsupported file extension")
