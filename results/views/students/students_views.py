import os

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404
from django.views.generic import TemplateView

from results.views.utils import Result, get_exam_results_from_user
from utils.get_exams import get_exam, get_object_or_404
from utils.sidebar_mixin import SideBarMixin, login_required
from utils.user_type import check_teacher

User = get_user_model()


@login_required(login_url='profiles:login', redirect_field_name='next')
def python_download_view(request, id, path):
    user = request.user

    result = get_object_or_404(
        Result.objects.prefetch_related('user', 'question__exam__author'),
        id=id, solution_file=path)

    check_teacher(user, result.user.username, result.question.exam)

    file_path = os.path.join(settings.MEDIA_ROOT, path)
    try:
        file_name = file_path.split('/')[-1]
        response = FileResponse(open(file_path, 'rb'), content_type='text/x-python')  # noqa:E501
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'  # noqa:E501

        return response

    except FileNotFoundError:
        raise Http404()


class ResultsStudentView(SideBarMixin, TemplateView):
    template_name = 'results/pages/results_student.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        exam_name = kwargs['exam']
        username = kwargs['username']

        user = get_object_or_404(User, username=username)
        exam = get_exam(exam_name)

        check_teacher(self.request.user, username, exam)

        results = get_exam_results_from_user(user, exam)

        total_score = sum(r['scores']['score_obtained']
                          for r in results.values())
        total_max_score = sum(r['scores']['max_score']
                              for r in results.values())

        context.update({
            'results': results,
            'student': f'{user.first_name} {user.last_name}',
            'exam': exam,
            'total_score': total_score,
            'total_max_score': total_max_score,
        })

        return context


class ResultsStudentOverView(SideBarMixin, TemplateView):
    template_name = 'results/pages/results_overview.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)

        username = kwargs['username']
        user = get_object_or_404(User, username=username)

        if self.request.user != user:
            raise PermissionDenied

        results = Result.objects.filter(user=user).order_by('-id')

        exams = {}
        for result in results.prefetch_related('question', 'question__exam'):
            exam = result.question.exam
            exams[exam.slug] = exam.name

        context.update({
            'exams': exams,
        })

        return context
