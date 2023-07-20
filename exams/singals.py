import os

from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Question


def delete_file(file):
    file_path = file.path

    if os.path.exists(file_path):
        os.remove(file_path)


@receiver(post_delete, sender=Question)
def post_delete_question(sender, instance, **kwargs):
    if instance.statement_pdf:
        delete_file(instance.statement_pdf)
    if instance.answer_zip:
        delete_file(instance.answer_zip)
