from django.shortcuts import render

# Create your views here.
from datetime import datetime, timedelta
from django.utils import timezone
from .models import Notification
from courses.models import Session
from rest_framework.permissions import IsAuthenticated
from students.authentication import StudentJWTAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


def send_upcoming_session_reminders():
    now = timezone.now()
    reminder_time = now + timedelta(minutes=10)

    sessions = Session.objects.filter(
        date=reminder_time.date(),
        time__hour=reminder_time.hour,
        time__minute=reminder_time.minute
    )
    for session in sessions:
        students = session.course.students.all()
        for student in students:
            Notification.objects.get_or_create(
                user=student,
                type='session_reminder',
                session=session,
                defaults={
                    'message': f"Reminder: You have a session for '{session.course.name}' at {session.time.strftime('%H:%M')}"
                }
            )
def send_absent_session_reminders():
    now = timezone.now()
    reminder_time = now + timedelta(minutes=10)

    sessions = Session.objects.filter(
        date=reminder_time.date(),
        time__hour=reminder_time.hour,
        time__minute=reminder_time.minute
    )

    for session in sessions:
        enrolled_students = session.course.students.all()
        attended_students = session.attended.all()

        absent_students = enrolled_students.exclude(id__in=attended_students.values_list('id', flat=True))

        for student in absent_students:
            Notification.objects.get_or_create(
                user=student,
                type='absent',
                session=session,
                defaults={
                    'message': f"Reminder: You have a session for '{session.course.name}' at {session.time.strftime('%H:%M')} and you haven't attended yet."
                }
            )

class MyNotificationsAPIView(APIView):
    authentication_classes = [StudentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        send_upcoming_session_reminders()
        send_absent_session_reminders
        notifications = request.user.notifications.all()
        data = [{
            "id": n.id,
            "type": n.type,
            "message": n.message,
            "session_id": n.session.id if n.session else None,
            "read": n.read,
            "created_at": n.created_at,
        } for n in notifications]

        return Response(data)

class MarkAllNotificationsReadAPIView(APIView):
    authentication_classes = [StudentJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        updated_count = Notification.objects.filter(user=request.user, read=False).update(read=True)
        return Response({"detail": f"{updated_count} notifications marked as read."}, status=status.HTTP_200_OK)

