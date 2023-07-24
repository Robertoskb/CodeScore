from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404

from exams.models import Exam


def get_exam_by_author(exam_name, author):
    exam = get_object_or_404(
        Exam.objects.prefetch_related('questions', 'author'),
        slug=exam_name)

    if exam.author != author:
        raise PermissionDenied

    return exam


def get_exam(exam_name, check_available=False):
    exam = get_object_or_404(
        Exam.objects.prefetch_related('questions', 'author'),
        slug=exam_name)

    if check_available and exam.available is False:
        raise Http404()

    return exam


def get_exam_by_code(code):
    exam = get_object_or_404(
        Exam.objects.prefetch_related('questions'),
        code=code, available=True)

    return exam
