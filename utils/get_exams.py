from django.http import Http404
from django.shortcuts import get_object_or_404

from exams.models import Exam


def get_exam(exam_name, check_avaliable=False):
    exam = get_object_or_404(
        Exam.objects.prefetch_related('questions'),
        slug=exam_name)

    if check_avaliable and exam.avaliable is False:
        raise Http404()

    return exam
