from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

from utils.tests.base import BaseTestUser

User = get_user_model()


class CustomUserModelTestCase(TestCase, BaseTestUser):
    """Test suit for the custom User model"""

    def setUp(self) -> None:
        self.active_regular_user = self.get_test_active_regularuser()
        self.inactive_regular_user = self.get_test_inactive_regularuser()
        self.super_user = self.get_test_superuser()
        self.staff_user = self.get_test_staffuser()

    def test_active_regular_user_creation(self):
        """test creaton of regular user"""
        user = self.active_regular_user
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.email, self.regularuser_active_data.email)
        self.assertTrue(user.check_password(self.regularuser_active_data.password))
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)

    def test_inactive_regular_user_creation(self):
        """test creaton of regular inactive user"""
        user = self.inactive_regular_user
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.email, self.regularuser_inactive_data.email)
        self.assertTrue(user.check_password(self.regularuser_inactive_data.password))
        self.assertEqual(user.is_active, False)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)

    def test_superuser_creation(self):
        """test creaton of super user"""
        user = self.super_user
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.email, self.superuser_data.email)
        self.assertTrue(user.check_password(self.superuser_data.password))
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, True)

    def test_staffuser_creation(self):
        """test creaton of staff user"""
        user = self.staff_user
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.email, self.staffuser_data.email)
        self.assertTrue(user.check_password(self.staffuser_data.password))
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, False)

    def test_email_field_validation(self):
        """Test email validation."""
        # Test required field
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="admin123")

        # Test invalid email format
        with self.assertRaises(ValueError):
            User.objects.create_user(email="invalid_email", password="admin123")

        # Test duplicate email address
        with self.assertRaises(IntegrityError):
            User.objects.create_user(**dict(vars(self.regularuser_active_data)))

    def test_first_name_and_last_name_handling(self):
        """Test if first_name and last name get properly timed."""
        self.assertEqual(
            self.active_regular_user.first_name, self.regularuser_active_data.first_name
        )
        self.assertEqual(
            self.active_regular_user.last_name, self.regularuser_active_data.last_name
        )

        # Test trimming of leading and trailing spaces
        user = User.objects.create_user(
            email="test2@example.com",
            password="admin123",
            first_name="   John   ",
            last_name="   Doe   ",
        )
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

    def test_full_name_properties(self):
        """Test full name porperty of the model."""
        self.assertEqual(
            self.active_regular_user.get_full_name,
            f"{self.regularuser_active_data.first_name.title()} {self.regularuser_active_data.last_name.title()}",
        )

    def test_short_name_properties(self):
        """Test short name porperty of the model."""
        self.assertEqual(
            self.active_regular_user.get_short_name,
            self.regularuser_active_data.first_name,
        )

    def test_user_activation(self):
        """Test user activation porperty of the model."""
        self.active_regular_user.is_active = False
        self.active_regular_user.save()
        self.assertFalse(self.active_regular_user.is_active)

        # Activate the user
        self.active_regular_user.activate_user
        self.assertTrue(self.active_regular_user.is_active)

    def test_string_representation(self):
        """Test str representation of the of the model."""
        self.assertEqual(
            str(self.active_regular_user), self.regularuser_active_data.email
        )

    def test_model_verbose_names(self):
        """Test meta atributes of the model."""
        self.assertEqual(User._meta.verbose_name, ("user"))
        self.assertEqual(User._meta.verbose_name_plural, ("users"))
