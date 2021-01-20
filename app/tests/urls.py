from django.urls import path

from . import views

urlpatterns = [
    path('', views.TestListView.as_view(), name='list'),
    path('add/', views.TestCreateView.as_view(), name='create'),
    path('<int:pk>/', views.TestDetailView.as_view(), name='detail'),
    path('<int:pk>/edit/', views.TestUpdateView.as_view(), name='update'),
    path('<int:pk>/process/', views.test_process, name='process'),
]
