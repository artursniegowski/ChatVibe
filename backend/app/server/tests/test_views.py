import uuid

from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from server.models import Category, Server
from server.serializers import ServerSerializer, CategorySerializer
from utils.tests.base import BaseTestUser

class CategoryViewSetTest(TestCase):
    """Test suit for CategoryViewSet."""
    @classmethod
    def setUpTestData(cls) -> None:
        # Create sample data for testing
        cls.category1 = Category.objects.create(
            name="Test Category 1", description="Test Description 1"
        )
        cls.category2 = Category.objects.create(
            name="Test Category 2", description="Test Description 2"
        )
    
    def setUp(self) -> None:
        # Initialize the test client
        self.client = APIClient()
        
    def test_list_categories_all(self):
        url = reverse("server:category-list")
        response = self.client.get(url)
        # check if response is as expected
        self.assertEqual(response.status_code, 200)
        # Serialize the queried categories
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        # Compare the serialized data with the response data
        self.assertEqual(response.data, serializer.data)

class ServerViewSetTest(TestCase, BaseTestUser):
    @classmethod
    def setUpTestData(cls):
        # Create sample data for testing
        cls.user = cls().get_test_active_regularuser()
        cls.user2 = cls().get_test_staffuser()
        cls.category = Category.objects.create(
            name="Test Category", description="Test Description"
        )
        cls.server = Server.objects.create(
            name="Test Server", owner=cls.user, category=cls.category
        )
        cls.server.member.add(cls.user, cls.user2)

    def setUp(self):
        # Initialize the test client
        self.client = APIClient()

    def test_list_servers_all(self):
        url = reverse("server:server-list")
        response = self.client.get(url)
        servers = Server.objects.all()
        # Serialize the queried servers
        serializer = ServerSerializer(servers, many=True)
        # Compare the serialized data with the response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)

    def test_list_servers_with_category_filter(self):
        url = reverse("server:server-list")
        data = {"category": self.category.name}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.server.name)
        self.assertEqual(response.data[0]["description"], self.server.description)

    def test_list_servers_with_category_none_existing_filter(self):
        url = reverse("server:server-list")
        data = {"category": "notexisting"}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_servers_by_user(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)
        url = reverse("server:server-list")
        data = {"by_user": "true"}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.server.name)
        self.assertEqual(response.data[0]["owner"], self.user.id)

    def test_list_servers_by_user_without_authentication(self):
        url = reverse("server:server-list")
        data = {"by_user": "true"}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 403)

    def test_list_servers_by_serverId(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)
        url = reverse("server:server-list")
        data = {"by_serverId": self.server.id}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.server.name)
        self.assertEqual(response.data[0]["owner"], self.user.id)

    def test_list_servers_by_serverId_without_authentication(self):
        url = reverse("server:server-list")
        data = {"by_serverId": self.server.id}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 403)

    def test_list_servers_by_serverId_not_existing(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)
        url = reverse("server:server-list")
        data = {"by_serverId": uuid.uuid4()}
        response = self.client.get(url, data)
        # bad request
        self.assertEqual(response.status_code, 400)

    def test_list_servers_by_serverId_wrong_format(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)
        url = reverse("server:server-list")
        data = {"by_serverId": 123}
        response = self.client.get(url, data)
        # bad request
        self.assertEqual(response.status_code, 400)

    def test_list_servers_with_num_members(self):
        url = reverse("server:server-list")
        data = {"with_num_members": "true"}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("num_members", response.data[0])
        num_members = response.data[0]["num_members"]
        self.assertIsInstance(num_members, int)
        self.assertEqual(num_members, 2)

    def test_list_servers_without_members(self):
        url = reverse("server:server-list")
        data = {"with_num_members": "false"}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("num_members", response.data)

    def test_list_servers_qty_only_one(self):
        url = reverse("server:server-list")
        data = {"qty": 2}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_list_servers_qty_total_2(self):
        url = reverse("server:server-list")
        data = {"qty": 2}
        Server.objects.create(
            name="Test Server 2", owner=self.user, category=self.category
        )
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_servers_qty_total_over_max(self):
        data = {"qty": 2}
        Server.objects.create(
            name="Test Server 2", owner=self.user, category=self.category
        )
        Server.objects.create(
            name="Test Server 3", owner=self.user, category=self.category
        )
        url = reverse("server:server-list")
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_list_servers_qty_wrong_number_negative(self):
        url = reverse("server:server-list")
        data = {"qty": -1}
        Server.objects.create(
            name="Test Server 2", owner=self.user, category=self.category
        )
        Server.objects.create(
            name="Test Server 3", owner=self.user, category=self.category
        )
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 400)

    def test_list_servers_qty_wrong_number_zero_not_positive(self):
        url = reverse("server:server-list")
        data = {"qty": 0}
        Server.objects.create(
            name="Test Server 2", owner=self.user, category=self.category
        )
        Server.objects.create(
            name="Test Server 3", owner=self.user, category=self.category
        )
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 400)

    def test_list_servers_qty_wrong_number_format(self):
        url = reverse("server:server-list")
        data = {"qty": "dsa"}
        Server.objects.create(
            name="Test Server 2", owner=self.user, category=self.category
        )
        Server.objects.create(
            name="Test Server 3", owner=self.user, category=self.category
        )
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, 400)
