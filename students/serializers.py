# student/serializers.py
from utils.validators.validators import validate_image  # Adjust path as needed
from rest_framework import serializers
from .models import Student
from django.contrib.auth.hashers import make_password
import os

class StudentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["student_id", "name", "level", "avatar"]

    def create(self, validated_data):
        # Automatically use student_id as the password (hashed)
        raw_password = validated_data["student_id"]
        validated_data["password"] = make_password(raw_password)
        return super().create(validated_data)
    def validate_avatar(self, value):
        return validate_image(value, max_size_mb=2)

class StudentLoginSerializer(serializers.Serializer):
    student_id = serializers.CharField()
    password = serializers.CharField(write_only=True)


class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [ "avatar"]
        extra_kwargs = {
            "avatar": {"required": False},
        }
    def validate_avatar(self, value):
        return validate_image(value, max_size_mb=2)

class StudentChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

class StudentUpdateAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["name", "level", "attendance"]
        

class StudentSetPasswordSerializer(serializers.Serializer):
    student_id = serializers.CharField()
    new_password = serializers.CharField(min_length=6, write_only=True)

    def validate_student_id(self, value):
        if not Student.objects.filter(student_id=value).exists():
            raise serializers.ValidationError("Student not found.")
        return value

    def update_password(self):
        student_id = self.validated_data["student_id"]
        new_password = self.validated_data["new_password"]

        student = Student.objects.get(student_id=student_id)
        student.password = make_password(new_password)
        student.save()
        return student
    
class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["student_id", "name", "level", "avatar", "attendance"]

