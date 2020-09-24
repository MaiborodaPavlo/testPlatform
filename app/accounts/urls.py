from django.conf.urls import url
from django.contrib.auth import views
from . import views

urlpatterns = [
    # url(r'^login/$', views.user_login, name='login'),
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^login/$', .views.login, name='login'),
    url(r'^logout/$', django.contrib.auth.views.logout, name='logout'),
]
