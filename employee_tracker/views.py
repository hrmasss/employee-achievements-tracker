from rest_framework import status, viewsets, filters
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from .models import Employee, Department, Achievement
from .serializers import (
    UserSerializer,
    LoginSerializer,
    EmployeeSerializer,
    DepartmentSerializer,
    AchievementSerializer,
)


class RegisterView(APIView):
    """
    API view for user registration.
    """

    permission_classes = [AllowAny]

    @extend_schema(request=UserSerializer, responses={201: UserSerializer})
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {"token": token.key, "user_id": user.pk, "email": user.email},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API view for user login.
    """

    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginSerializer,
        responses={200: "Login successful", 401: "Invalid credentials"},
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
            )
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {"token": token.key, "user_id": user.pk, "email": user.email}
                )
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    API view for user logout.
    """

    @extend_schema(request=None, responses={200: "Logout successful"})
    def post(self, request):
        if request.user.is_authenticated:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(
            {"error": "User not logged in."}, status=status.HTTP_401_UNAUTHORIZED
        )


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows employee CRUD operations.
    """

    queryset = Employee.objects.all().order_by("-id")
    serializer_class = EmployeeSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["department"]
    search_fields = ["name", "email"]
    ordering_fields = ["name", "department__name"]

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows department CRUD operations.
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AchievementViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows achievement CRUD operations.
    """

    queryset = Achievement.objects.all()
    serializer_class = AchievementSerializer

    def get_queryset(self):
        return self.queryset.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
