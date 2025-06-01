from django.db import models

from login_auth.models import CustomUser



class Course(models.Model):
    name = models.CharField(max_length=255)
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date = models.DateField()
    day = models.CharField(max_length=20)  # e.g., 'Monday', 'Wednesday'
    time = models.TimeField()
    level = models.CharField(max_length=100)
    number_of_sessions = models.PositiveIntegerField()
    image = models.ImageField(upload_to='courses/',blank=True,null=True)

    def __str__(self):
        return self.name
    class Meta:
        db_table= 'courses'

class Session(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions')
    date = models.DateField()
    time = models.TimeField()
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.course.name} - {self.date}"
    class Meta:
        db_table= 'sessions'