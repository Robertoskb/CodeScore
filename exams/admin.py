from django.contrib import admin

from .models import Exam, Question, Result


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    ...


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    ...
