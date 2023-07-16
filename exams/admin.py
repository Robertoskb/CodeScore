from django.contrib import admin

from .models import Exam, Question


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    readonly_fields = ('code',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    ...
