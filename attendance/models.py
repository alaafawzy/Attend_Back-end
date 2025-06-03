from django.db import models
from students.models import Student
from courses.models import Course,Session

class AttendanceRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('denied', 'Denied'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'attendance_requests'
        unique_together = ('student', 'session')

    def __str__(self):
        return f"{self.student} -> {self.session} ({self.status})"