from django.views.generic import TemplateView
from utils.sidebar_mixin import SideBarMixin


class ResultsStudentView(SideBarMixin, TemplateView):
    template_name = 'results/pages/results_student.html'
