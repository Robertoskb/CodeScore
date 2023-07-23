import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView, TemplateView

from exams.forms import PythonFileForm
from exams.models import Question
from results.models import Result
from results.views.utils import get_questions_maximum_score
from students.forms import PINform
from utils.corrector import corrector
from utils.get_exams import get_exam_by_code
from utils.sidebar_mixin import SideBarMixin

required = login_required(login_url='profiles:login',
                          redirect_field_name='next')


@login_required(login_url='profiles:login', redirect_field_name='next')
def pdf_view(request, question, path):
    get_object_or_404(Question.objects.prefetch_related('exam'),
                      slug=question, exam__available=True, statement_pdf=path)

    file_path = os.path.join(settings.MEDIA_ROOT, path)
    try:
        file_name = file_path.split('/')[-1]
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')  # noqa:E501
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'  # noqa:E501

        return response

    except FileNotFoundError:
        raise Http404()


class SearchPINView(SideBarMixin, FormView):
    template_name = 'students/pages/search_pin.html'
    form_class = PINform

    def form_valid(self, form):
        pin = form.cleaned_data['pin'].upper()

        self.success_url = reverse('students:exam', args=(pin,))

        return super().form_valid(form)


class ExamView(SideBarMixin, TemplateView):
    template_name = 'students/pages/questions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pin = kwargs['pin']

        exam = get_exam_by_code(code=pin)

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
        pin = self.kwargs['pin']

        exam = get_exam_by_code(pin)

        question = get_object_or_404(Question, slug=question_name)

        best_result = get_questions_maximum_score(self.request.user, question)

        context.update({
            'question': question,
            'exam': exam,
            'best_result': best_result,
        })

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        user = self.request.user
        question = self.get_context_data()['question']

        existing_results = Result.objects.filter(
            user=user, question=question, need_resubmission=False).count()

        if existing_results > 49:
            form.add_error(
                'python_file', 'Número máximo de submissões atingido')

            return self.form_invalid(form)

        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        context = self.get_context_data()

        exam = context['exam']
        question = context['question']

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

        self.success_url = reverse_lazy(
            'students:question', args=(exam.slug, question.slug))

        best_result = context['best_result']

        if best_result is None or score > best_result.score_obtained:
            context['best_result'] = result

        return self.render_to_response(context)
