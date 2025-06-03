from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register('sessions', SessionViewSet, basename='session')

urlpatterns = [
    path('', include(router.urls)),
    path('my-courses/', MyCoursesAPIView.as_view(), name='my-courses'),
    path('my-courses/<int:course_id>/sessions/', MyCourseSessionsAPIView.as_view(), name='my-course-sessions'),
    path('my-calendar/', WeeklyCalendarAPIView.as_view(), name='my-calendar'),
    path('calendar/<int:day>/', DailyCalendarAPIView.as_view(), name='my-calendar'),

]
