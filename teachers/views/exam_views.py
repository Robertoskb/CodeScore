from django.urls import reverse
from django.views.generic import FormView, TemplateView

from exams.forms import Exam, ExamForm

from .teacher_mixin import TeacherMixin


class TeacherExams(TeacherMixin, TemplateView):
    template_name = 'teachers/pages/exams.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["exams"] = Exam.objects.all()

        return context


class CreateExam(TeacherMixin, FormView):
    template_name = 'teachers/pages/exam_form.html'
    form_class = ExamForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form_title'] = 'Cadastro de Prova'
        context['cancel_url'] = reverse('teachers:exams')

        return context

    def form_valid(self, form):
        exam = form.save()

        self.success_url = reverse('teachers:exam', args=(exam.slug,))

        return super().form_valid(form)
