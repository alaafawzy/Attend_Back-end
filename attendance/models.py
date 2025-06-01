from django.db import models
from students.models import Student
from courses.models import Course,Session

class AttendanceRecord(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='attendance_records')
    timestamp = models.DateTimeField(auto_now_add=True)
    is_present = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.course.course_name} - {self.timestamp}"
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE,related_name='attendance_student')
    session = models.ForeignKey(Session, on_delete=models.CASCADE,related_name='attendanded')
    attended = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'session')