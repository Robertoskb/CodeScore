from django.contrib import admin

from .models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'question', 'exam',
                    'score_obtained', 'max_score', 'date')

    def exam(self, obj):
        return obj.question.exam
