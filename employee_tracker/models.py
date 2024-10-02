from django.db import models


class Department(models.Model):
    """
    Represents a department in the organization.
    """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    """
    Represents an employee in the organization.
    """

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    achievements = models.ManyToManyField("Achievement", through="AchievementEmployee")

    def __str__(self):
        return self.name


class Achievement(models.Model):
    """
    Represents an achievement that can be awarded to employees.
    """

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class AchievementEmployee(models.Model):
    """
    Represents the relationship between an employee and their achievements,
    including the date the achievement was awarded.
    """

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    achievement_date = models.DateField()

    class Meta:
        unique_together = ("employee", "achievement")

    def __str__(self):
        return f"{self.employee.name} - {self.achievement.name}"
