from django.contrib import admin

from .models import Exam, Question


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'available', 'code',)

    list_display_links = ('name',)

    list_editable = ('available',)
    readonly_fields = ('code',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    ...
