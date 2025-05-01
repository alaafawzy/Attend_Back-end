# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login,logout,authenticate
from rest_framework import generics
from .serializers import *
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from django.middleware.csrf import get_token
from django.contrib.auth import get_user_model
from utils.permissions.permissions import IsAdminOrSelf
from django.shortcuts import get_object_or_404

User = get_user_model()

class AddMemberView(generics.CreateAPIView):
    serializer_class = CreateMemberSerializer
    permission_classes = [IsAdminUser]

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password changed successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class SetNewPasswordView(APIView):
    permission_classes = [IsAdminUser]  # Or a custom permission class

    def post(self, request):
        serializer = SetNewPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    authentication_classes = []  # Allow unauthenticated access
    permission_classes = []      # Allow anyone to access

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)  # creates session and sets sessionid cookie
            csrf_token = get_token(request)  # generate CSRF token
            return Response({
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name,
                    "role": user.role,
                    "avatar": request.build_absolute_uri(user.avatar.url) if user.avatar else None,
                    "is_staff": user.is_staff
                },
                "csrfToken": csrf_token
            })
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)
    
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"})
    
class UserListView(APIView):
    permission_classes = [IsAdminUser]  # Change this to fit your role system

    def get(self, request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many=True, context={"request": request})
        return Response(serializer.data)


class UserUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSelf]

    def patch(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        self.check_object_permissions(request, user)

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

