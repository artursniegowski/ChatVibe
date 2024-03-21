from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class FileSizeValidator:
    """
    Validator class to check the size of an uploaded file.

    Attributes:
        max_file_size (int): The maximum allowed size of the file, in KB or MB.
        size_in_mb (bool): Indicates whether the `max_file_size` is in MB. \
            If True, the size is in MB; otherwise, it's in KB.
        message (str): The error message to be raised when the file size exceeds the maximum allowed size.
        code (str): The error code associated with the validation error.

    Args:
        max_file_size (int): The maximum allowed size of the file. Default is 500 KB.
        size_in_mb (bool): If True, `max_file_size` represents MB; otherwise, it represents KB. Default is False.
        message (str): Optional. The custom error message to be raised. Default is a generic error message.
        code (str): Optional. The custom error code. Default is "file_size_exceeded".
    """

    max_file_size: int = 500  # KB or MB
    size_in_mb: bool = False  # default false, so the size is by default in KB,
    # if size_in_mb = True, then the max_file_size will represent MB
    message = _(
        "The file size exceed the maximum allowed size %(allowed_size)s. The image was %(image_size)s."
    )
    code = "file_size_exceeded"

    def __init__(self, max_file_size=None, size_in_mb=None, message=None, code=None):
        if max_file_size is not None:
            self.max_file_size = max_file_size
        if size_in_mb is not None:
            self.size_in_mb = size_in_mb
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, file: UploadedFile) -> None:
        """
        Validates the size of the uploaded file.
        """
        allowed_size = (
            self.max_file_size * 1024 * 1024
            if self.size_in_mb
            else self.max_file_size * 1024
        )
        if file.size > allowed_size:
            units = "MB" if self.size_in_mb else "KB"
            params = {
                "allowed_size": f"{allowed_size} {units}",
                "image_size": f"{file.size} {units}",
            }
            raise ValidationError(self.message, code=self.code, params=params)

    def __eq__(self, other):
        """
        Compares two validators for equality.
        """
        return (
            isinstance(other, FileSizeValidator)
            and (self.max_file_size == other.max_file_size)
            and (self.size_in_mb == other.size_in_mb)
            and (self.message == other.message)
            and (self.code == other.code)
        )
