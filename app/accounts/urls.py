from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('update/<int:pk>/', views.UserUpdate.as_view(), name='update'),
]
