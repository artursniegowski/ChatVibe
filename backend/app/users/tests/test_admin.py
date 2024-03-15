from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from utils.tests.base import BaseTestUser

User = get_user_model()


class AdminTestCase(TestCase, BaseTestUser):
    """Test Suit for the custom admin"""

    def setUp(self):
        self.client = Client()
        # login as admin
        self.admin_user = self.get_test_superuser()
        self.client.force_login(self.admin_user)
        # create a regular user in the database
        self.user = self.get_test_active_regularuser()

    def test_admin_accessible(self):
        """Test that users are listed on page."""
        url = reverse("admin:users_user_changelist")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.user.first_name)
        self.assertContains(res, self.user.last_name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """Test the edit user page works"""
        url = reverse("admin:users_user_change", args=(self.user.id,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = {
            "email": "updated@example.com",
            "first_name": "Updated",
            "last_name": "User",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.email, data["email"])
        self.assertEqual(updated_user.first_name, data["first_name"])
        self.assertEqual(updated_user.last_name, data["last_name"])

    def test_create_user_page(self):
        """Test the create user page works"""
        url = reverse("admin:users_user_add")
        res = self.client.get(url)
        # makign sure the page responds with 200 - status OK
        self.assertEqual(res.status_code, 200)
        # adding a user
        data = {
            "email": "test@example2.com",
            "password1": "testpassword",
            "password2": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "is_active": True,
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(User.objects.filter(email=data["email"]).exists())

    def test_user_search(self):
        """Test search functionality in the user list page."""
        url = reverse("admin:users_user_changelist") + "?q=" + self.user.email
        response = self.client.get(url)
        self.assertContains(response, self.user.email)

    def test_validation(self):
        """Test validation messages in the admin forms."""
        url = reverse("admin:users_user_add")
        # Submit form with invalid data
        data = {
            "email": "invalid-email",  # Invalid email format
            "password1": "testpassword",
            "password2": "testpassword",
            "first_name": "Test",
            "last_name": "User",
            "is_active": True,
        }
        response = self.client.post(url, data)

        # Check if the form is not valid
        self.assertFalse(response.context["adminform"].form.is_valid())
        # Check if the form has a specific field error for the 'email' field
        self.assertTrue("email" in response.context["adminform"].form.errors)
