from django.views.generic import TemplateView

from results.models import User
from results.views.utils import get_sum_of_highest_scores
from teachers.views import TeacherMixin
from utils.get_exams import get_exam
from utils.user_type import check_teacher


class ExamResultsView(TeacherMixin, TemplateView):
    template_name = 'results/pages/exam_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam_name = kwargs['exam']

        exam = get_exam(exam_name)

        check_teacher(self.request.user, exam.author, exam)

        users = User.objects.all()

        sums = ((user, get_sum_of_highest_scores(user, exam)) for user in users)  # noqa: E501

        users_score = ((user, score) for user, score in sums if score is not None)  # noqa: E501

        context['users_score'] = users_score
        context['exam'] = exam

        return context
