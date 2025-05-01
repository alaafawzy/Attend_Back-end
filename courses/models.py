from django.db import models

class Course(models.Model):
    course_id = models.CharField(max_length=20, unique=True)
    course_name = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    instructor_id = models.CharField(max_length=50)
    instructor_name = models.CharField(max_length=100)

    def __str__(self):
        return self.course_name
