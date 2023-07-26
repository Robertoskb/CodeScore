from django.views.generic import TemplateView

from .teacher_mixin import TeacherMixin


class TeacherTutorial(TeacherMixin, TemplateView):
    template_name = 'teachers/pages/tutorial.html'
