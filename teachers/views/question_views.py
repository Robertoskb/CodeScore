from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView, UpdateView, View

from exams.forms import Question, QuestionForm
from utils.get_exams import get_exam, get_object_or_404

from .teacher_mixin import TeacherMixin


class TeacherQuestions(TeacherMixin, TemplateView):
    template_name = 'teachers/pages/questions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exam_name = kwargs['exam']

        exam = get_exam(exam_name)
        questions = exam.questions.all().order_by('-id')

        context.update({
            'exam': exam,
            'questions': questions,
        })

        return context


class CreateQuestion(TeacherMixin, FormView):
    template_name = 'teachers/pages/question_form.html'
    form_class = QuestionForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        name = request.POST.get('name')
        exam = self.get_context_data(**kwargs)['exam']

        if Question.objects.filter(name=name, exam=exam).exists():
            form.add_error(
                'name', 'Uma questão com esse nome já foi incluída nesta prova')  # noqa:E501

            return self.form_invalid(form)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        exam = get_exam(self.kwargs['exam'])

        question = form.save(commit=False)
        question.exam = exam
        question.save()

        self.success_url = reverse('teachers:exam', args=(exam.slug,))

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam = get_exam(self.kwargs['exam'])

        context.update({
            'exam': exam,
            'form_title': 'Cadastro de Questão',
            'cancel_url': reverse('teachers:exam', args=(exam.slug,)),
        })

        return context


class UpdateQuestion(TeacherMixin, UpdateView):
    template_name = 'teachers/pages/question_form.html'
    form_class = QuestionForm
    model_class = Question

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        exam = get_exam(self.kwargs['exam'])

        context['form_title'] = 'Editar de Questão'
        context['cancel_url'] = reverse('teachers:exam', args=(exam.slug,))

        return context

    def form_valid(self, form):
        exam = form.save().exam

        self.success_url = reverse('teachers:exam', args=(exam.slug,))

        return super().form_valid(form)

    def get_object(self, queryset=None):
        exam = get_exam(self.kwargs['exam'])
        questions = exam.questions.all()

        return get_object_or_404(questions, slug=self.kwargs['question'])


class DeleteQuestion(TeacherMixin, View):
    def post(self, *args, **kwargs):
        pk = self.request.POST.get('question', None)
        question = get_object_or_404(Question, pk=pk)
        exam = question.exam

        question.delete()

        return redirect(reverse('teachers:exam', args=(exam.slug,)))
