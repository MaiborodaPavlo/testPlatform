import nested_admin
from django.contrib import admin

from .models import (
    Test,
    Question,
    Answer,
    Result)


class AnswerInline(nested_admin.NestedStackedInline):
    model = Answer
    max_num = 4


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    inlines = [AnswerInline]


class ResultsInline(nested_admin.NestedTabularInline):
    model = Result


class TestAdmin(nested_admin.NestedModelAdmin):
    inlines = [ResultsInline, QuestionInline]


admin.site.register(Test, TestAdmin)
