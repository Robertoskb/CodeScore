import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView

from exams.forms import PythonFileForm
from exams.models import Exam
from results.models import Result
from utils.corrector import corrector
from utils.get_exams import get_exam
from utils.sidebar_mixin import SideBarMixin

required = login_required(login_url='profiles:login',
                          redirect_field_name='next')


@login_required(login_url='profiles:login', redirect_field_name='next')
def pdf_view(request, path):
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    try:
        file_name = file_path.split('/')[-1]
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')  # noqa:E501
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'  # noqa:E501

        return response

    except FileNotFoundError:
        raise Http404()


class ExamsView(SideBarMixin, TemplateView):
    template_name = 'students/pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['exams'] = Exam.objects.filter(avaliable=True)

        return context


class ExamView(SideBarMixin, TemplateView):
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


class QuestionView(SideBarMixin, FormView):
    template_name = 'students/pages/question.html'
    form_class = PythonFileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        question_name = self.kwargs['question']
        exam_name = self.kwargs['exam']

        exam = get_exam(exam_name, check_avaliable=True)

        questions = exam.questions.all()
        question = get_object_or_404(questions, slug=question_name)

        context.update({
            'question': question,
            'exam': exam,
            'questions': questions,
        })

        return context

    def form_valid(self, form):
        context = self.get_context_data()

        exam = context['exam']
        question = context['question']

        self.success_url = reverse_lazy(
            'students:question', args=(exam.slug, question.slug))

        python_file = form.cleaned_data['python_file']

        logs = corrector(python_file, question.answer_zip.path)
        score, max_score = logs.pop().values()

        result = Result.objects.create(user=self.request.user,
                                       question=question,
                                       score_obtained=score,
                                       max_score=max_score,
                                       solution_file=python_file)

        result.save()

        context['logs'] = logs
        context['score_message'] = f'{score}/{max_score}'

        return self.render_to_response(context)
