# student/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import *
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.permissions.permissions import IsAdmin 
from rest_framework.authentication import SessionAuthentication

class RegisterStudentView(APIView):
    authentication_classes = [SessionAuthentication]  # Admin uses cookies/session
    permission_classes = [IsAuthenticated, IsAdmin]
    def post(self, request):
        serializer = StudentRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Student registered successfully"}, status=201)
        return Response(serializer.errors, status=400)


class StudentLoginView(APIView):
    def post(self, request):
        serializer = StudentLoginSerializer(data=request.data)
        if serializer.is_valid():
            student_id = serializer.validated_data["student_id"]
            password = serializer.validated_data["password"]

            try:
                student = Student.objects.get(student_id=student_id)
                if check_password(password, student.password):
                    refresh = RefreshToken.for_user(student)
                    return Response({
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                        "student_id": student.student_id,
                        "name": student.name,
                        "avatar": student.avatar,
                        "level": student.level,
                        "attendance": student.attendance
                    })
                else:
                    return Response({"error": "Invalid credentials"}, status=401)
            except Student.DoesNotExist:
                return Response({"error": "Student not found"}, status=404)
        return Response(serializer.errors, status=400)


class StudentUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        student = get_object_or_404(Student, id=request.user.id)
        serializer = StudentUpdateSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully"})
        return Response(serializer.errors, status=400)


class StudentChangePasswordView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = StudentChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            student = get_object_or_404(Student, id=request.user.id)
            if not check_password(serializer.validated_data["old_password"], student.password):
                return Response({"error": "Incorrect old password"}, status=400)
            student.password = make_password(serializer.validated_data["new_password"])
            student.save()
            return Response({"message": "Password updated successfully"})
        return Response(serializer.errors, status=400)

class AdminUpdateStudentView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, student_id):
        try:
            student = Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = StudentUpdateAdminSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Student updated successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AdminSetStudentPasswordView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = StudentSetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.update_password()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminDeleteStudentView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request, student_id):
        try:
            student = Student.objects.get(student_id=student_id)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

        student.delete()
        return Response({"message": "Student deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class AdminListStudentsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        students = Student.objects.all()
        serializer = StudentListSerializer(students, many=True)
        return Response(serializer.data)
