import zipfile
from random import choice
from string import ascii_uppercase

from autoslug import AutoSlugField
from django.contrib.auth import get_user_model
from django.db import models

from utils.validators import pdf_validator, zip_validator

User = get_user_model()


def get_code(length):
    return ''.join(choice(ascii_uppercase) for _ in range(length))


class Exam(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', unique=True)
    code = models.CharField(max_length=6, unique=True, editable=False)
    available = models.BooleanField(default=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='exams')

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
    modified = models.BooleanField(default=False, editable=False)

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
