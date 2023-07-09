from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

User = get_user_model()


class Exam(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    avaliable = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)


class Question(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    statement_pdf = models.FileField(upload_to='exams/statements/')
    answer_zip = models.FileField(upload_to='exams/answers/')
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        return super().save(*args, **kwargs)

    class Meta:
        unique_together = ('slug', 'exam')


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    score_obtained = models.IntegerField()
    max_score = models.IntegerField()
    solution_file = models.FileField(upload_to='exams/solutions')

    def clean(self):
        if self.score_obtained > self.max_score:
            raise ValidationError(
                "Pontuação obtida não pode ser maior do que a pontuação máxima.")  # noqa:E50

    def __str__(self):
        return f"{self.user} {self.question}"  # noqa:E501
