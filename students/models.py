from django.db import models
from django.contrib.auth.hashers import make_password, is_password_usable

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)  # store hashed
    level = models.CharField(max_length=50)
    avatar = models.ImageField(upload_to='student_avatars/', null=True, blank=True)

    attendance = models.PositiveIntegerField(default=5)  # New field!

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # if not self.pk or not is_password_usable(self.password):  # New or raw password
        #     self.password = make_password(self.password)
        super().save(*args, **kwargs)
    class Meta:
        db_table= 'student'
