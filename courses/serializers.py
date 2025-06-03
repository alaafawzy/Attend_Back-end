from rest_framework import serializers
from .models import *
from datetime import timedelta
import datetime
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
    def create(self, validated_data):
        course = super().create(validated_data)

        # Auto-enroll students with the same level
        matching_students = Student.objects.filter(level=course.level)
        course.students.set(matching_students)
        # Generate sessions automatically
        day_name = validated_data['day']  # e.g. 'Monday'
        session_date = validated_data['start_date']
        number = validated_data['number_of_sessions']
        session_time = validated_data['time']
        instructor = validated_data['instructor']

        weekday_number = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'].index(day_name)

        # Adjust to first correct day if needed
        while session_date.weekday() != weekday_number:
            session_date += timedelta(days=1)

        for _ in range(number):
            Session.objects.create(
                course=course,
                date=session_date,
                time=session_time,
                instructor=instructor
            )
            session_date += timedelta(days=7)

        return course

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'
        

class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'start_date', 'day', 'time', 'level', 'instructor','number_of_sessions','image']