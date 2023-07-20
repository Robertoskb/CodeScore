import os

from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Question


def delete_file(file):
    try:
        os.remove(file.path)
    except (ValueError, FileNotFoundError):
        ...


@receiver(post_delete, sender=Question)
def post_delete_question(sender, instance, **kwargs):
    delete_file(instance.statement_pdf)
    delete_file(instance.answer_zip)


@receiver(pre_save, sender=Question)
def post_pre_save_question(sender, instance, **kwargs):
    old_instance = Question.objects.filter(pk=instance.pk).first()

    if old_instance:
        old_pdf = old_instance.statement_pdf
        old_zip = old_instance.answer_zip

        if old_pdf != instance.statement_pdf:
            delete_file(old_pdf)
        if old_zip != instance.answer_zip:
            delete_file(old_zip)
