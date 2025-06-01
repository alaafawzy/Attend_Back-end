from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register('sessions', SessionViewSet, basename='session')

urlpatterns = [
    path('', include(router.urls)),
]
