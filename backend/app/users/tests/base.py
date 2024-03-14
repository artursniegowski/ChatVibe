from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()


class UserData:
    """stores users data"""

    def __init__(
        self, email: str, first_name: str, last_name: str, password: str
    ) -> None:
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password


class BaseTestUser:
    """base clas with custom users generated with the class"""

    def __init__(self) -> None:
        self.superuser_data: UserData = UserData(
            "test_superuser@test.com", "superuser_fn", "susperuser_ln", "superuser_pass"
        )
        self.staffuser_data: UserData = UserData(
            "test_staffuser@test.com", "staffuser_fn", "staffuser_ln", "staffuser_pass"
        )
        self.regularuser_inactive_data: UserData = UserData(
            "test_regularuser_inactive@test.com",
            "regularuser_inactive_fn",
            "regularuser_inactive_ln",
            "regularuser_inactive_pass",
        )
        self.regularuser_active_data: UserData = UserData(
            "test_regularuser_active@test.com",
            "regularuser_active_fn",
            "regularuser_active_ln",
            "regularuser_pass",
        )

    def get_test_superuser(self) -> User:
        """return a test supseruser"""
        data = dict(vars(self.superuser_data))
        data["is_superuser"] = True
        data["is_staff"] = True
        data["is_active"] = True
        data["password"] = make_password(data["password"])
        super_user, _ = User.objects.get_or_create(**data)
        return super_user

    def get_test_staffuser(self) -> User:
        """return a test staffuser"""
        data = dict(vars(self.staffuser_data))
        data["is_staff"] = True
        data["is_active"] = True
        data["password"] = make_password(data["password"])
        staffuser_user, _ = User.objects.get_or_create(**data)
        return staffuser_user

    def get_test_active_regularuser(self) -> User:
        """return a test regular"""
        data = dict(vars(self.regularuser_active_data))
        data["password"] = make_password(data["password"])
        active_regularuser, _ = User.objects.get_or_create(**data)
        return active_regularuser

    def get_test_inactive_regularuser(self) -> User:
        """return a test regular"""
        data = dict(vars(self.regularuser_inactive_data))
        data["password"] = make_password(data["password"])
        data["is_active"] = False
        inactive_regularuser, _ = User.objects.get_or_create(**data)
        return inactive_regularuser
