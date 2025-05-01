# users/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('add-new-member/', AddMemberView.as_view(), name='user-register'),
    path('change-password/', ChangePasswordView.as_view()),
    path('set-new-password/', SetNewPasswordView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("users/", UserListView.as_view(), name="user-list"),
    path("users/<int:user_id>/update/", UserUpdateView.as_view(), name="user-update"),

    # path('login/', LoginView.as_view(), name='token_obtain_pair'),
]
