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
    need_resubmission = models.BooleanField(default=False, editable=False)

    def clean(self):
        existing_results = Result.objects.filter(
            user=self.user, question=self.question).count()

        if existing_results > 50:
            raise ValidationError("Número máximo de submissões atingido")

        if self.score_obtained > self.max_score:
            raise ValidationError(
                "Pontuação obtida não pode ser maior do que a pontuação máxima.")  # noqa:E50

    def clean_solution_file(self):
        file = self.cleaned_data['solution_file']

        if not file.name.endswith('.py'):
            raise ValidationError('Submeta um arquivo python válio!')

        return file

    def __str__(self):
        return f"{self.user}"
