from django.db import models
from django.contrib.auth.hashers import make_password, is_password_usable
from courses.models import Course

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # store hashed
    level = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='student_avatars/', null=True, blank=True)
    # courses = models.ManyToManyField(Course, related_name='students')
    attendance = models.PositiveIntegerField(default=5)  # New field!

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # if not self.pk or not is_password_usable(self.password):  # New or raw password
        #     self.password = make_password(self.password)
        super().save(*args, **kwargs)
