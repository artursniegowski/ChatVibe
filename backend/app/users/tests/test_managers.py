from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase

User = get_user_model()


class UserManagerTests(TestCase):
    """Test suit for the custom user manager"""

    def test_create_user(self):
        """Test creating a regular user"""
        user = User.objects.create_user(
            email="test@example.com", password="password123"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password("password123"))

    def test_create_superuser(self):
        """Test creating a superuser"""
        superuser = User.objects.create_superuser(
            email="admin@example.com", password="admin123"
        )
        self.assertEqual(superuser.email, "admin@example.com")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)
        self.assertTrue(superuser.check_password("admin123"))

    def test_create_user_with_invalid_email(self):
        """Test creating a user with an invalid email"""
        with self.assertRaises(ValueError):
            User.objects.create_user(email="invalid_email", password="admin123")

    def test_create_superuser_with_invalid_email(self):
        """Test creating a superuser with an invalid email"""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email="invalid_email", password="admin123")

    def test_email_normalization_regular_user(self):
        """Test email normalization"""
        email = "Test.Email@Example.com"
        normalized_email = "Test.Email@example.com"
        user = User.objects.create_user(email=email, password="admin123")
        self.assertEqual(user.email, normalized_email)

    def test_email_normalization_super_user(self):
        """Test email normalization"""
        email = "Test.Email@Example.com"
        normalized_email = "Test.Email@example.com"
        user = User.objects.create_superuser(email=email, password="admin123")
        self.assertEqual(user.email, normalized_email)

    def test_email_normalization_edge_cases(self):
        """Test email normalization with edge cases"""
        test_cases = [
            ("Test.Email2@Example.com", "Test.Email2@example.com"),
            ("  Test.Email22@Example.com  ", "Test.Email22@example.com"),
            ("test.email222@example.com  ", "test.email222@example.com"),
            ("test.email2222@example.com", "test.email2222@example.com"),
        ]

        for email, expected_normalized_email in test_cases:
            user = User.objects.create_user(email=email, password="admin123")
            self.assertEqual(user.email, expected_normalized_email)

    def test_missing_email_regular_user(self):
        """Test missing email regularuser"""
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="password123")

    def test_missing_email_regular_superuser(self):
        """Test missing email superuser"""
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email="", password="password123")

    def test_with_perm_no_backend(self):
        """Test with_perm when backend is not provided"""
        with self.assertRaises(ValueError):
            User.objects.with_perm("some_perm")

    def test_with_perm_invalid_backend(self):
        """Test with_perm with an invalid backend"""
        with self.assertRaises(TypeError):
            User.objects.with_perm("some_perm", backend=123)

    def test_with_perm_single_backend(self):
        """Test with_perm with a single authentication backend"""
        User.objects._auth_backends = [ModelBackend()]
        result = User.objects.with_perm(
            "myapp.some_perm", backend="django.contrib.auth.backends.ModelBackend"
        )
        # Assuming none() returns an empty queryset
        self.assertEqual(len(result), len(User.objects.none()))

    def test_user_permissions(self):
        """Test user permissions"""
        # Create a user
        user = User.objects.create_user(email="test@example.com", password="admin123")
        # Obtain the permission content type
        content_type = ContentType.objects.get_for_model(
            User
        )  # Assuming permission is related to User model
        # Create the permission if it doesn't exist
        permission, _ = Permission.objects.get_or_create(
            codename="some_permission",
            content_type=content_type,
            defaults={"name": "Permission Name"},
        )
        # Add the permission to the user
        user.user_permissions.add(permission)
        # print("User permissions:", user.user_permissions.all())
        # print("Permission app label:", permission.content_type.app_label)
        # Check if the user has the permission
        self.assertTrue(user.has_perm("users.some_permission"))
