from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('notifications/', MyNotificationsAPIView.as_view(), name='my-notifications'),
    path('notifications/mark-all-read/', MarkAllNotificationsReadAPIView.as_view(), name='mark-all-notifications-read'),

]
