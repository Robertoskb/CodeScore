from django.contrib import admin

from .models import Exam, Question


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    ...


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    ...
