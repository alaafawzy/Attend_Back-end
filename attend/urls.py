from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/members/', include('login_auth.urls')),
    path('api/students/', include('students.urls')),
    path('api/', include('courses.urls')),
    path('api/attendance/', include('attendance.urls')),
    path('api/auth/', include('login_auth.urls')),
]
