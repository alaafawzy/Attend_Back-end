from django.db import models
from django.utils import timezone
from students.models import Student
from courses.models import Session
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('session_reminder', 'Session Reminder'),
        ('attendance_approved', 'Attendance Approved'),
        ('attendance_denied', 'Attendance Denied'),
        ('absent','Absent')
    )

    user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=30, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} - {self.type}"