from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView

from results.views.utils import get_exam_results_from_user
from utils.get_exams import get_exam, get_object_or_404
from utils.sidebar_mixin import SideBarMixin, get_user_type

User = get_user_model()


class ResultsStudentView(SideBarMixin, TemplateView):
    template_name = 'results/pages/results_student.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        exam_name = kwargs['exam']
        username = kwargs['username']

        user = get_object_or_404(User, username=username)
        exam = get_exam(exam_name)
        results = get_exam_results_from_user(user, exam)

        total_score = sum(r['score'] for r in results.values())

        context.update({
            'results': results,
            'student': f'{user.first_name} {user.last_name}',
            'exam': exam,
            'total_score': total_score,
        })

        return context

    def get(self, *args, **kwargs):
        user = self.request.user
        user_type = get_user_type(user)

        username_validation = user.username != kwargs['username']
        user_type_validation = 'admin' != user_type != 'teacher'

        if username_validation and user_type_validation:
            raise PermissionDenied

        return super().get(*args, **kwargs)
