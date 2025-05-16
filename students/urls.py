from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path("add-new-student/", RegisterStudentView.as_view(), name="student-register"),
    path("login/", StudentLoginView.as_view(), name="student-login"),
    path("update-avatar/", StudentUpdateView.as_view(), name="student-update-avatar"),
    path("change-password/", StudentChangePasswordView.as_view(), name="student-change-password"),
    path("update/<str:student_id>/", AdminUpdateStudentView.as_view(), name="student-update"),
    path("set-password/", AdminSetStudentPasswordView.as_view(), name="student-new-password"),
    path("<str:student_id>/delete/", AdminDeleteStudentView.as_view(), name="admin-delete-student"),
    path("", AdminListStudentsView.as_view(), name="admin-list-students"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh
    path('profile/', StudentProfileView.as_view(), name='student-profile'),  # Refresh


]
