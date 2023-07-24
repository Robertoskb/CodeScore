from django.contrib import admin

from .models import Exam, Question


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'available', 'author', 'code',)

    list_display_links = ('name',)

    list_editable = ('available',)
    readonly_fields = ('code',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_score', 'modified')
    list_display_links = ('name',)
    readonly_fields = ('max_score',)
