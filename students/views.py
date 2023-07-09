import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from exams.forms import PythonFileForm
from exams.models import Exam
from utils.corrector import corrigir
from utils.get_exams import get_exam
from utils.sidebar_mixin import SideBarMixin

required = login_required(login_url='profiles:login',
                          redirect_field_name='next')


@method_decorator(required, name='dispatch')
def pdf_view(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    try:
        file_name = file_path.split('/')[-1]
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')  # noqa:E501
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'  # noqa:E501

        return response

    except FileNotFoundError:
        raise Http404()


@method_decorator(required, name='dispatch')
class StudentViewBase(SideBarMixin, TemplateView):
    ...


class ExamsView(StudentViewBase):
    template_name = 'students/pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['exams'] = Exam.objects.all()

        return context


class ExamView(StudentViewBase):
    template_name = 'students/pages/questions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exam_name = kwargs['exam']

        exam = get_exam(exam_name, check_avaliable=True)

        questions = exam.questions.all()

        context.update({
            'exam': exam,
            'questions': questions,
        })

        return context


class QuestionView(StudentViewBase):
    template_name = 'students/pages/question.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        question_name = kwargs['question']
        exam_name = kwargs['exam']

        exam = get_exam(exam_name, check_avaliable=True)

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
