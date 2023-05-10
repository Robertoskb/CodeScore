from django.db import models
from django.utils.text import slugify


class Exam(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    avaliable = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    def save(self):
        if not self.slug:
            self.slug = slugify(self.title)


class Question(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    statement_pdf = models.FileField(upload_to='exams/statments/')
    answer_zip = models.FileField(upload_to='exams/answers/')
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.name

    def save(self):
        if not self.slug:
            self.slug = slugify(self.title)

    class Meta:
        unique_together = ('slug', 'exam')
