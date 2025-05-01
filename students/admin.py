from django.contrib import admin
from .models import Student  # تأكد إن الاسم صح لو الموديل في ملف مختلف

admin.site.register(Student)
