from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView, UpdateView, View

from exams.forms import Exam, ExamForm
from utils.get_exams import get_exam

from .teacher_mixin import TeacherMixin


class TeacherExams(TeacherMixin, TemplateView):
    template_name = 'teachers/pages/exams.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["exams"] = Exam.objects.all().order_by('-id')

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


class UpdateExam(TeacherMixin, UpdateView):
    template_name = 'teachers/pages/exam_form.html'
    form_class = ExamForm
    model = Exam
    success_url = reverse_lazy('teachers:exams')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['form_title'] = 'Editar Prova'
        context['cancel_url'] = reverse('teachers:exams')

        return context

    def get_object(self, queryset=None):
        return get_exam(self.kwargs['exam'])


class DeleteExam(TeacherMixin, View):
    def post(self, *args, **kwargs):
        exam = get_exam(self.request.POST.get('exam', None))

        exam.delete()

        return redirect(reverse('teachers:exams'))
