from django.test import TestCase
from django.db.utils import IntegrityError
from employee_tracker.models import (
    Department,
    Employee,
    Achievement,
    AchievementEmployee,
)


class ModelTestCase(TestCase):
    def setUp(self):
        """Create initial objects for testing."""
        self.department = Department.objects.create(name="IT")
        self.employee = Employee.objects.create(
            name="John Doe",
            email="john@example.com",
            phone="1234567890",
            address="123 Main St",
            department=self.department,
        )
        self.achievement = Achievement.objects.create(name="Employee of the Month")

    def test_department_creation(self):
        """Test that a Department object is created correctly."""
        self.assertEqual(self.department.name, "IT")

    def test_employee_creation(self):
        """Test that an Employee object is created correctly."""
        self.assertEqual(self.employee.name, "John Doe")
        self.assertEqual(self.employee.department, self.department)

    def test_achievement_creation(self):
        """Test that an Achievement object is created correctly."""
        self.assertEqual(self.achievement.name, "Employee of the Month")

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
        with self.assertRaises(IntegrityError):
            Department.objects.create(name="IT")  # Duplicate department name

        with self.assertRaises(IntegrityError):
            Employee.objects.create(
                name="Jane Doe",
                email="john@example.com",  # Duplicate email
                phone="0987654321",
                address="456 Elm St",
                department=self.department,
            )
