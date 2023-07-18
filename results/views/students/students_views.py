from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView

from utils.sidebar_mixin import SideBarMixin, get_user_type


class ResultsStudentView(SideBarMixin, TemplateView):
    template_name = 'results/pages/results_student.html'

    def get(self, *args, **kwargs):
        user_type = get_user_type(self.request.user)

        if 'admin' != user_type != 'teacher':
            raise PermissionDenied

        return super().get(*args, **kwargs)
