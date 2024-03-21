from django.test import Client, TestCase
from django.urls import reverse

from server.models import Category, Channel, Server
from utils.tests.base import BaseTestUser


class CategoryAdminTestCase(TestCase, BaseTestUser):
    """Test Suit for the Category admin"""

    def setUp(self):
        self.client = Client()
        # login as admin
        self.admin_user = self.get_test_superuser()
        self.client.force_login(self.admin_user)
        # create a Category to view data
        self.category = Category.objects.create(
            name="Test Category", description="Test Description"
        )

    def test_admin_accessible(self):
        """Test that categories are listed on page."""
        url = reverse("admin:server_category_changelist")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.category.name)
        # March 15, 2024, 6:32 p.m
        formatted_created = self.category.created.strftime("%B %d, %Y, %#I:%M %#p")
        self.assertContains(res, formatted_created)
        formatted_modified = self.category.modified.strftime("%B %d, %Y, %#I:%M %#p")
        self.assertContains(res, formatted_modified)

    def test_edit_category_page(self):
        """Test the edit category page works"""
        url = reverse("admin:server_category_change", args=(self.category.id,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = {
            "name": "updated_category",
            "description": "Updated",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        updated_category = Category.objects.get(id=self.category.id)
        self.assertEqual(updated_category.name, data["name"])
        self.assertEqual(updated_category.description, data["description"])

    def test_create_category_page(self):
        """Test the create Category page works"""
        url = reverse("admin:server_category_add")
        res = self.client.get(url)
        # makign sure the page responds with 200 - status OK
        self.assertEqual(res.status_code, 200)
        # adding a user
        data = {
            "name": "new_category",
            "description": "new_description",
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(Category.objects.filter(name=data["name"]).exists())

    def test_category_search(self):
        """Test search functionality in the category list page."""
        url = reverse("admin:server_category_changelist") + "?q=" + self.category.name
        response = self.client.get(url)
        self.assertContains(response, self.category.name)

    def test_validation(self):
        """Test validation messages in the category forms."""
        url = reverse("admin:server_category_add")
        # Submit form with invalid data
        data = {
            "name": "",  # Invalid name
        }
        response = self.client.post(url, data)

        # Check if the form is not valid
        self.assertFalse(response.context["adminform"].form.is_valid())
        # Check if the form has a specific field error for the 'email' field
        self.assertTrue("name" in response.context["adminform"].form.errors)

    def test_detail_category_page(self):
        """Test the detail channel page."""
        url = reverse("admin:server_category_change", args=(self.category.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.category.id)
        self.assertContains(response, self.category.name)
        self.assertContains(response, self.category.description)
        formatted_created = self.category.created.strftime("%B %d, %Y, %#I:%M %#p")
        self.assertContains(response, formatted_created)
        formatted_modified = self.category.modified.strftime("%B %d, %Y, %#I:%M %#p")
        self.assertContains(response, formatted_modified)


class ChannelAdminTestCase(TestCase, BaseTestUser):
    """Test Suit for the Channel admin"""

    def setUp(self):
        self.client = Client()
        # login as admin
        self.admin_user = self.get_test_superuser()
        self.user = self.get_test_active_regularuser()
        self.client.force_login(self.admin_user)
        # create a Category to view data
        self.category = Category.objects.create(
            name="Test Category", description="Test Description"
        )
        self.server = Server.objects.create(
            name="Test server", owner=self.user, category=self.category
        )
        self.channel = Channel.objects.create(
            name="First Channel", owner=self.user, server=self.server
        )

    def test_admin_accessible(self):
        """Test that chanells are listed on page."""
        url = reverse("admin:server_channel_changelist")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.channel.name)
        self.assertContains(res, self.channel.owner)
        self.assertContains(res, self.channel.server)
        # March 15, 2024, 6:32 p.m
        formatted_created = self.channel.created.strftime("%B %d, %Y, %#I:%M %#p")
        self.assertContains(res, formatted_created)
        formatted_modified = self.channel.modified.strftime("%B %d, %Y, %#I:%M %#p")
        self.assertContains(res, formatted_modified)

    def test_edit_channel_page(self):
        """Test the edit channel page works"""
        url = reverse("admin:server_channel_change", args=(self.channel.id,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = {
            "name": "updated_channel",
            "topic": "Updated",
            "owner": self.channel.owner.id,
            "server": self.channel.server.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        updated_channel = Channel.objects.get(id=self.channel.id)
        self.assertEqual(updated_channel.name, data["name"])
        self.assertEqual(updated_channel.topic, data["topic"])

    def test_create_channel_page(self):
        """Test the create channel page works"""
        url = reverse("admin:server_channel_add")
        res = self.client.get(url)
        # makign sure the page responds with 200 - status OK
        self.assertEqual(res.status_code, 200)
        # adding a user
        data = {
            "name": "new_channel_1",
            "topic": "new_channel",
            "owner": self.user.id,
            "server": self.server.id,
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(Channel.objects.filter(name=data["name"]).exists())

    def test_channel_search(self):
        """Test search functionality in the channel list page."""
        url = reverse("admin:server_channel_changelist") + "?q=" + self.channel.name
        response = self.client.get(url)
        self.assertContains(response, self.channel.name)
        url = (
            reverse("admin:server_channel_changelist")
            + "?q="
            + self.channel.owner.email
        )
        response = self.client.get(url)
        self.assertContains(response, self.channel.owner.email)
        url = (
            reverse("admin:server_channel_changelist")
            + "?q="
            + self.channel.server.name
        )
        response = self.client.get(url)
        self.assertContains(response, self.channel.server.name)

    def test_validation(self):
        """Test validation messages in the channel forms."""
        url = reverse("admin:server_channel_add")
        # Submit form with invalid data
        data = {
            "name": "",  # Invalid name
            # missing owner and server
        }
        response = self.client.post(url, data)

        # Check if the form is not valid
        self.assertFalse(response.context["adminform"].form.is_valid())
        # Check if the form has a specific field error for the 'email' field
        self.assertTrue("name" in response.context["adminform"].form.errors)
        self.assertTrue("owner" in response.context["adminform"].form.errors)
        self.assertTrue("server" in response.context["adminform"].form.errors)

    def test_detail_channel_page(self):
        """Test the detail channel page."""
        url = reverse("admin:server_channel_change", args=(self.channel.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.channel.id)
        self.assertContains(response, self.channel.name)
        self.assertContains(response, self.channel.owner.email)
        self.assertContains(response, self.channel.topic)
        self.assertContains(response, self.channel.server.name)
        formatted_created = self.channel.created.strftime("%B %d, %Y, %#I:%M %#p")
        self.assertContains(response, formatted_created)
        formatted_modified = self.channel.modified.strftime("%B %d, %Y, %#I:%M %#p")
        self.assertContains(response, formatted_modified)


class ServerAdminTestCase(TestCase, BaseTestUser):
    """Test Suit for the Server admin"""

    def setUp(self):
        self.client = Client()
        # login as admin
        self.admin_user = self.get_test_superuser()
        self.user = self.get_test_active_regularuser()
        self.client.force_login(self.admin_user)
        # create a Category to view data
        self.category = Category.objects.create(
            name="Test Category", description="Test Description"
        )
        self.server = Server.objects.create(
            name="Test server",
            owner=self.user,
            category=self.category,
            description="simple server",
        )

    def test_admin_accessible(self):
        """Test that Server are listed on page."""
        url = reverse("admin:server_server_changelist")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, self.server.name)
        self.assertContains(res, self.server.owner)
        self.assertContains(res, self.server.category)
        # March 15, 2024, 6:32 p.m
        formatted_created = self.server.created.strftime("%B %d, %Y, %#I:%M %#p")
        self.assertContains(res, formatted_created)
        formatted_modified = self.server.modified.strftime("%B %d, %Y, %#I:%M %#p")
        self.assertContains(res, formatted_modified)

    def test_edit_server_page(self):
        """Test the edit server page works"""
        url = reverse("admin:server_server_change", args=(self.server.id,))
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        data = {
            "name": "updated_server",
            "description": "Updated",
            "owner": self.server.owner.id,
            "category": self.server.category.id,
            "member": [self.user.id],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        updated_server = Server.objects.get(id=self.server.id)
        self.assertEqual(updated_server.name, data["name"])
        self.assertEqual(updated_server.description, data["description"])

    def test_create_server_page(self):
        """Test the create server page works"""
        url = reverse("admin:server_server_add")
        res = self.client.get(url)
        # makign sure the page responds with 200 - status OK
        self.assertEqual(res.status_code, 200)
        # adding a user
        data = {
            "name": "new server greate",
            "description": "New server",
            "owner": self.user.id,
            "category": self.category.id,
            "member": [self.user.id],
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, 302)
        self.assertTrue(Server.objects.filter(name=data["name"]).exists())

    def test_server_search(self):
        """Test search functionality in the server list page."""
        url = reverse("admin:server_server_changelist") + "?q=" + self.server.name
        response = self.client.get(url)
        self.assertContains(response, self.server.name)
        url = (
            reverse("admin:server_server_changelist") + "?q=" + self.server.owner.email
        )
        response = self.client.get(url)
        self.assertContains(response, self.server.owner.email)
        url = (
            reverse("admin:server_server_changelist")
            + "?q="
            + self.server.category.name
        )
        response = self.client.get(url)
        self.assertContains(response, self.server.category.name)

    def test_validation(self):
        """Test validation messages in the server forms."""
        url = reverse("admin:server_server_add")
        # Submit form with invalid data
        data = {
            "name": "",  # Invalid name
            # missing owner and category
        }
        response = self.client.post(url, data)

        # Check if the form is not valid
        self.assertFalse(response.context["adminform"].form.is_valid())
        # Check if the form has a specific field error for the 'email' field
        self.assertTrue("name" in response.context["adminform"].form.errors)
        self.assertTrue("owner" in response.context["adminform"].form.errors)
        self.assertTrue("category" in response.context["adminform"].form.errors)

    def test_detail_server_page(self):
        """Test the detail server page."""
        url = reverse("admin:server_server_change", args=(self.server.id,))
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, self.server.id)
        self.assertContains(response, self.server.name)
        self.assertContains(response, self.server.owner.email)
        self.assertContains(response, self.server.category.name)
        self.assertContains(response, self.server.description)
        for member in self.server.member.all():
            self.assertContains(response, member.email)
        formatted_created = self.server.created.strftime("%B %d, %Y, %#I:%M %#p")
        self.assertContains(response, formatted_created)
        formatted_modified = self.server.modified.strftime("%B %d, %Y, %#I:%M %#p")
        self.assertContains(response, formatted_modified)
