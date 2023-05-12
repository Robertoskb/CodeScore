import os

from django.conf import settings
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from utils.corrector import corrigir
from utils.get_exams import get_exam

from .forms import PythonFileForm
from .models import Exam


def pdf_view(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    try:
        file_name = file_path.split('/')[-1]
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')  # noqa:E501
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'  # noqa:E501

        return response

    except FileNotFoundError:
        raise Http404()


class HomeView(TemplateView):
    template_name = 'exams/pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['exams'] = Exam.objects.all()

        return context


class ExamView(TemplateView):
    template_name = 'exams/pages/questions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exam_name = kwargs['exam']

        exam = get_exam(exam_name)
        questions = exam.questions.all()

        context.update({
            'exam': exam,
            'questions': questions,
        })

        return context


class QuestionView(TemplateView):
    template_name = 'exams/pages/question.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        question_name = kwargs['question']
        exam_name = kwargs['exam']

        exam = get_exam(exam_name)
        questions = exam.questions.all()
        question = get_object_or_404(questions, slug=question_name)

        context.update({
            'question': question,
            'form': PythonFileForm(),
            'exam': exam,
            'questions': questions,
        })

        return context

    def post(self, request, *args, **kwargs):
        form = PythonFileForm(request.POST, request.FILES)

        context = self.get_context_data(**kwargs)

        if form.is_valid():
            question_name = kwargs['question']
            exam_name = kwargs['exam']

            exam = get_exam(exam_name)
            question = get_object_or_404(exam.questions, slug=question_name)

            python_file = form.cleaned_data['python_file']
            logs = corrigir(python_file, question.answer_zip.path)

            context['logs'] = logs

        return self.render_to_response(context)
