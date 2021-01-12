from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    login_view,
    dashboard,
    signup_view,
    UserUpdate,
)

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', signup_view, name='signup'),
    path('update/<int:pk>/', UserUpdate.as_view(), name='update'),
]
