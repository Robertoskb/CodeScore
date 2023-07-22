import zipfile
from random import choice
from string import ascii_uppercase

from autoslug import AutoSlugField
from django.db import models

from utils.validators import pdf_validator, zip_validator


def get_code(length):
    return ''.join(choice(ascii_uppercase) for _ in range(length))


class Exam(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)
    code = models.CharField(max_length=6, unique=True, editable=False)
    available = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.pk is None:
            length = 6

            self.code = get_code(length)
            while Exam.objects.filter(code=self.code).exists():
                self.code = get_code(length)

        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Question(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    statement_pdf = models.FileField(
        upload_to='exams/statements/', validators=(pdf_validator,))
    answer_zip = models.FileField(
        upload_to='exams/answers/', validators=(zip_validator,))
    exam = models.ForeignKey(
        Exam, on_delete=models.CASCADE, related_name='questions')
    max_score = models.IntegerField(editable=False, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        with zipfile.ZipFile(self.answer_zip.path) as zip_file:
            self.max_score = sum(1 for name in zip_file.namelist()
                                 if name.endswith('in')) * 10

            super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'exam')
