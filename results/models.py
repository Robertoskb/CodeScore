from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from exams.models import Question

User = get_user_model()


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    score_obtained = models.IntegerField()
    max_score = models.IntegerField()
    solution_file = models.FileField(upload_to='exams/solutions/')

    def clean(self):
        if self.score_obtained > self.max_score:
            raise ValidationError(
                "Pontuação obtida não pode ser maior do que a pontuação máxima.")  # noqa:E50

    def __str__(self):
        return f"{self.user}"
