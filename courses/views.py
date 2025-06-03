from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from students.authentication import StudentJWTAuthentication
from rest_framework.permissions import IsAuthenticated
from students.models import Student
from datetime import datetime, timedelta
from django.db.models.functions import ExtractWeekDay


class CourseListCreateView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class MyCoursesAPIView(APIView):
    authentication_classes = [StudentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        student=request.user

        courses = student.courses.all()
        serializer = StudentCourseSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MyCourseSessionsAPIView(APIView):
    authentication_classes = [StudentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        student = request.user

        try:
            course = Course.objects.get(id=course_id, students=student)
        except Course.DoesNotExist:
            return Response({"detail": "Course not found or you are not enrolled."}, status=status.HTTP_404_NOT_FOUND)

        sessions = course.sessions.all().order_by('date', 'time')
        total_sessions = sessions.count()

        if total_sessions == 0:
            return Response({"detail": "This course has no sessions."}, status=status.HTTP_204_NO_CONTENT)

        attended_sessions = set(
            course.sessions.filter(attended=student).values_list('id', flat=True)
        )

        # Counter to calculate progressive attendance
        attended_count = 0
        data = []

        for index, session in enumerate(sessions, start=1):
            attended = session.id in attended_sessions
            if attended:
                attended_count += 1

            progressive_percentage = round((attended_count / total_sessions) * 100, 2)

            data.append({
                "id": session.id,
                "course": course.name,
                "date": session.date,
                "time": session.time,
                "instructor_id": session.instructor.id,
                "attended": attended,
                "attendance_progress": progressive_percentage
            })

        overall_percentage = round((len(attended_sessions) / total_sessions) * 100, 2)

        return Response({
            "course": course.name,
            "course_id": course.id,
            "total_sessions": total_sessions,
            "attended_sessions": len(attended_sessions),
            "overall_percentage": overall_percentage,
            "sessions": data
        })


class WeeklyCalendarAPIView(APIView):
    authentication_classes = [StudentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        week_param = request.query_params.get('week')
        if not week_param:
            return Response({"detail": "Missing `week` query parameter (YYYY-MM-DD)."}, status=400)

        try:
            week_start = datetime.strptime(week_param, "%Y-%m-%d").date()
        except ValueError:
            return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        week_end = week_start + timedelta(days=6)

        student=request.user

        sessions = Session.objects.filter(
            course__students=student,
            date__range=(week_start, week_end)
        ).order_by('date', 'time').distinct()

        data = []
        for session in sessions:
            data.append({
                "id": session.id,
                "course": session.course.name,
                "course_id": session.course.id,
                "date": session.date,
                "time": session.time,
                "instructor_id": session.instructor.id,
                "attended": student in session.attended.all(),
            })

        return Response(data, status=200)

class DailyCalendarAPIView(APIView):
    authentication_classes = [StudentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request,day):
        day_param=day

        try:
            day_num = int(day_param)
            if day_num < 1 or day_num > 7:
                raise ValueError()
        except ValueError:
            return Response({"detail": "`day` must be a number between 1 (Saturday) and 7 (Friday)."}, status=400)

        # Calculate the current week's Monday
        day_map = {
            1: 7,  # Saturday -> 7
            2: 1,  # Sunday -> 1
            3: 2,  # Monday -> 2
            4: 3,  # Tuesday -> 3
            5: 4,  # Wednesday -> 4
            6: 5,  # Thursday -> 5
            7: 6   # Friday -> 6
        }
        django_weekday = day_map[day_num]

        student = request.user

        # Get courses where student is enrolled and that have at least one session on the weekday
        courses = Course.objects.filter(
            students=student,
            sessions__date__isnull=False  # to join sessions table
        ).annotate(
            weekday=ExtractWeekDay('sessions__date')
        ).filter(
            weekday=django_weekday
        ).distinct()

        data = []
        for course in courses:
            data.append({
                "id": course.id,
                "name": course.name,
                "instructor_id": course.instructor.name,
                "level": course.level,
            })

        return Response(data)