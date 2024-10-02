from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Employee, Department, Achievement, AchievementEmployee


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model, used for registration.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    """

    email = serializers.EmailField()
    password = serializers.CharField()


class DepartmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Department model.
    """

    class Meta:
        model = Department
        fields = ["id", "name"]


class AchievementSerializer(serializers.ModelSerializer):
    """
    Serializer for the Achievement model.
    """

    class Meta:
        model = Achievement
        fields = ["id", "name"]


class AchievementEmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for the AchievementEmployee model, managing employee-achievement relationships.
    """

    achievement = AchievementSerializer(read_only=True)
    achievement_id = serializers.PrimaryKeyRelatedField(
        queryset=Achievement.objects.all(), source="achievement", write_only=True
    )

    class Meta:
        model = AchievementEmployee
        fields = ["id", "achievement", "achievement_id", "achievement_date"]


class EmployeeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Employee model.
    """

    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(), source="department", write_only=True
    )
    achievements = AchievementEmployeeSerializer(
        source="achievementemployee_set", many=True, read_only=True
    )

    class Meta:
        model = Employee
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "address",
            "department",
            "department_id",
            "achievements",
        ]

    def create(self, validated_data):
        achievements_data = self.context["request"].data.get("achievements", [])
        employee = Employee.objects.create(**validated_data)
        for achievement_data in achievements_data:
            AchievementEmployee.objects.create(employee=employee, **achievement_data)
        return employee

    def update(self, instance, validated_data):
        achievements_data = self.context["request"].data.get("achievements", [])
        instance = super().update(instance, validated_data)
        instance.achievementemployee_set.all().delete()
        for achievement_data in achievements_data:
            AchievementEmployee.objects.create(employee=instance, **achievement_data)
        return instance
