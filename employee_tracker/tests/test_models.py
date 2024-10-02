from django.test import TestCase
from django.db import transaction
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from employee_tracker.models import (
    Department,
    Employee,
    Achievement,
    AchievementEmployee,
)


class ModelTestCase(TestCase):
    def setUp(self):
        """Create initial objects for testing."""

        self.user = User.objects.create_user(username="testuser", password="12345")

        self.department = Department.objects.create(name="IT", created_by=self.user)
        self.employee = Employee.objects.create(
            name="John Doe",
            email="john@example.com",
            phone="1234567890",
            address="123 Main St",
            department=self.department,
            created_by=self.user,
        )
        self.achievement = Achievement.objects.create(
            name="Employee of the Month", created_by=self.user
        )

    def test_department_creation(self):
        """Test that a Department object is created correctly."""
        self.assertEqual(self.department.name, "IT")
        self.assertEqual(self.department.created_by, self.user)

    def test_employee_creation(self):
        """Test that an Employee object is created correctly."""
        self.assertEqual(self.employee.name, "John Doe")
        self.assertEqual(self.employee.department, self.department)
        self.assertEqual(self.employee.created_by, self.user)

    def test_achievement_creation(self):
        """Test that an Achievement object is created correctly."""
        self.assertEqual(self.achievement.name, "Employee of the Month")
        self.assertEqual(self.achievement.created_by, self.user)

    def test_achievement_employee_creation(self):
        """Test that an AchievementEmployee object is created correctly."""
        achievement_employee = AchievementEmployee.objects.create(
            employee=self.employee,
            achievement=self.achievement,
            achievement_date="2023-01-01",
        )
        self.assertEqual(achievement_employee.employee, self.employee)
        self.assertEqual(achievement_employee.achievement, self.achievement)

    def test_unique_constraints(self):
        """Test that unique constraints raise IntegrityError."""
        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Department.objects.create(
                    name="IT", created_by=self.user
                )  # Duplicate department name

        with transaction.atomic():
            with self.assertRaises(IntegrityError):
                Employee.objects.create(
                    name="Jane Doe",
                    email="john@example.com",  # Duplicate email
                    phone="0987654321",
                    address="456 Elm St",
                    department=self.department,
                    created_by=self.user,
                )
