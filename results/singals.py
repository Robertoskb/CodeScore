import os

from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Result


@receiver(post_delete, sender=Result)
def post_delete_result(sender, instance, **kwargs):
    if instance.solution_file:
        file_path = instance.solution_file.path

        if os.path.exists(file_path):
            os.remove(file_path)
