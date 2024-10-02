from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from employee_tracker.models import Department, Employee, Achievement
from django.contrib.auth.models import User


class APITestCase(TestCase):
    def setUp(self):
        """Create a test user and initial data for API tests."""
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        self.department = Department.objects.create(name="HR", created_by=self.user)
        self.achievement = Achievement.objects.create(
            name="Best Performance", created_by=self.user
        )

    def test_create_employee(self):
        """Test the creation of a new Employee object via the API."""
        url = reverse("employee-list")
        data = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "phone": "1234567890",
            "address": "123 Main St",
            "department_id": self.department.id,
            "achievements": [
                {
                    "achievement_id": self.achievement.id,
                    "achievement_date": "2023-01-01",
                }
            ],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.get().name, "Jane Doe")
        self.assertEqual(Employee.objects.get().created_by, self.user)

    def test_get_employee_list(self):
        """Test retrieving the list of Employee objects via the API."""
        Employee.objects.create(
            name="John Doe",
            email="john@example.com",
            phone="0987654321",
            address="456 Elm St",
            department=self.department,
            created_by=self.user,
        )
        url = reverse("employee-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_update_employee(self):
        """Test updating an existing Employee object via the API."""
        employee = Employee.objects.create(
            name="John Doe",
            email="john@example.com",
            phone="0987654321",
            address="456 Elm St",
            department=self.department,
            created_by=self.user,
        )
        url = reverse("employee-detail", kwargs={"pk": employee.id})
        data = {
            "name": "John Updated",
            "email": "john@example.com",
            "phone": "1111111111",
            "address": "789 Oak St",
            "department_id": self.department.id,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Employee.objects.get(id=employee.id).name, "John Updated")

    def test_delete_employee(self):
        """Test deleting an Employee object via the API."""
        employee = Employee.objects.create(
            name="John Doe",
            email="john@example.com",
            phone="0987654321",
            address="456 Elm St",
            department=self.department,
            created_by=self.user,
        )
        url = reverse("employee-detail", kwargs={"pk": employee.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)

    def test_register_user(self):
        """Test user registration via the API."""
        url = reverse("register")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)

    def test_login_user(self):
        """Test user login via the API."""
        url = reverse("login")
        data = {"username": "testuser", "password": "12345"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_logout_user(self):
        """Test user logout via the API."""
        url = reverse("logout")
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
