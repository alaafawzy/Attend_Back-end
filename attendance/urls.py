from django.urls import path
from .views import *

urlpatterns = [
    path('request-attendance/<int:session_id>/', RequestAttendanceAPIView.as_view(), name='request-attendance'),
    path('review-request/<int:request_id>/', ReviewAttendanceRequestAPIView.as_view(), name='review-attendance-request'),
    path('attendance-requests/', ListAttendanceRequestsAPIView.as_view(), name='admin-attendance-requests'),

]
