from autoslug import AutoSlugField
from django.db import models


class Exam(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    avaliable = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class Question(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    statement_pdf = models.FileField(upload_to='exams/statements/')
    answer_zip = models.FileField(upload_to='exams/answers/')
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'exam')
