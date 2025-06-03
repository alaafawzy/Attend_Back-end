from rest_framework import generics
from .models import *
from .serializers import *

from django.utils import timezone
from notification.models import Notification
from rest_framework.permissions import IsAuthenticated
from students.authentication import StudentJWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from courses.models import Session
from utils.permissions.permissions import IsAdmin 


def approve_attendance_request(request_obj):
    request_obj.status = 'approved'
    request_obj.reviewed_at = timezone.now()
    request_obj.save()
    request_obj.session.attended.add(request_obj.student)
    Notification.objects.create(
        user=request_obj.student,
        type='attendance_approved',
        session=request_obj.session,
        message=f"Your request to attend the session '{request_obj.session.course.name}' on {request_obj.session.date} has been approved."
    )

def deny_attendance_request(request_obj):
    request_obj.status = 'denied'
    request_obj.reviewed_at = timezone.now()
    request_obj.save()

    Notification.objects.create(
        user=request_obj.student,
        type='attendance_denied',
        session=request_obj.session,
        message=f"Your request to attend the session '{request_obj.session.course.name}' on {request_obj.session.date} has been denied."
    )
# class AttendanceListCreateView(generics.ListCreateAPIView):
#     queryset = AttendanceRecord.objects.all()
#     serializer_class = AttendanceRecordSerializer
class RequestAttendanceAPIView(APIView):
    authentication_classes = [StudentJWTAuthentication]
    permission_classes = [IsAuthenticated] # Use StudentJWTAuthentication if needed

    def post(self, request, session_id):
        student = request.user

        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return Response({"detail": "Session not found."}, status=status.HTTP_404_NOT_FOUND)

        # Ensure student is enrolled in the course
        if not session.course.students.filter(id=student.id).exists():
            return Response({"detail": "You are not enrolled in this course."}, status=status.HTTP_403_FORBIDDEN)

        # Prevent duplicate requests
        request_obj, created = AttendanceRequest.objects.get_or_create(
            student=student,
            session=session,
            defaults={'status': 'pending'}
        )

        if not created:
            return Response({"detail": "Request already exists.", "status": request_obj.status})

        return Response({"detail": "Attendance request submitted."}, status=status.HTTP_201_CREATED)
    
class ReviewAttendanceRequestAPIView(APIView):
    permission_classes = [IsAuthenticated,IsAdmin]

    def post(self, request, request_id):
        action = request.data.get("action")  # "approve" or "deny"

        try:
            request_obj = AttendanceRequest.objects.get(id=request_id)
        except AttendanceRequest.DoesNotExist:
            return Response({"detail": "Request not found."}, status=status.HTTP_404_NOT_FOUND)

        # if request_obj.status != "pending":
        #     return Response({"detail": f"Request already {request_obj.status}."}, status=status.HTTP_400_BAD_REQUEST)

        if action == "approve":
            approve_attendance_request(request_obj)
        elif action == "deny":
            deny_attendance_request(request_obj)
        else:
            return Response({"detail": "Invalid action. Use 'approve' or 'deny'."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": f"Request {action}d successfully."}, status=status.HTTP_200_OK)

class ListAttendanceRequestsAPIView(APIView):
    permission_classes = [IsAuthenticated,IsAdmin]

    def get(self, request):
        requests = AttendanceRequest.objects.select_related('student', 'session', 'session__course').all()

        data = []
        for r in requests:
            data.append({
                "id": r.id,
                "status": r.status,
                "created_at": r.created_at,
                "reviewed_at": r.reviewed_at,
                "student": {
                    "id": r.student.id,
                    "username": r.student.name,
                    "level": r.student.level
                },
                "session": {
                    "id": r.session.id,
                    "date": r.session.date,
                    "time": r.session.time,
                    "course": {
                        "id": r.session.course.id,
                        "name": r.session.course.name
                    }
                }
            })

        return Response(data, status=status.HTTP_200_OK)
    
