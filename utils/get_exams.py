from django.shortcuts import get_object_or_404

from exams.models import Exam


def get_exam(exam_name):
    return get_object_or_404(
        Exam.objects.prefetch_related('questions'),
        slug=exam_name)
