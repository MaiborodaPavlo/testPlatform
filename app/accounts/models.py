from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse_lazy


class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(unique=True, max_length=255)
    dob = models.DateField(blank=True, null=True)
    info = models.TextField(blank=True, null=True)
    avatar = models.ImageField(blank=True, null=True, upload_to='avatars')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def get_absolute_url(self):
        return reverse_lazy('accounts:dashboard')
