from django.contrib import admin

from tests.models import Result
from .models import User


class ResultsInline(admin.StackedInline):
    model = Result


class UserAdmin(admin.ModelAdmin):
    inlines = [ResultsInline]


admin.site.register(User, UserAdmin)
