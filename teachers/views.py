from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView

from exams.forms import Exam, ExamForm, Question, QuestionForm
from utils.get_exams import get_exam, get_object_or_404


class TeacherExams(TemplateView):
    template_name = 'teachers/pages/exams.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["exams"] = Exam.objects.all()

        return context


class TeacherQuestions(TemplateView):
    template_name = 'teachers/pages/questions.html'

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


class CreateExam(FormView):
    template_name = 'teachers/pages/exam_form.html'
    form_class = ExamForm

    def form_valid(self, form):
        exam = form.save()

        self.success_url = reverse('teachers:exam', args=(exam.slug,))

        return super().form_valid(form)


class CreateQuestion(FormView):
    template_name = 'teachers/pages/question_form.html'
    form_class = QuestionForm

    def form_valid(self, form):
        exam = form.save().exam

        self.success_url = reverse('teachers:exam', args=(exam.slug,))

        return super().form_valid(form)


class UpdateQuestion(UpdateView):
    template_name = 'teachers/pages/question_form.html'
    form_class = QuestionForm
    model_class = Question

    def form_valid(self, form):
        exam = form.save().exam

        self.success_url = reverse('teachers:exam', args=(exam.slug,))

        return super().form_valid(form)

    def get_object(self, queryset=None):
        exam = get_exam(self.kwargs['exam'])
        questions = exam.questions.all()

        return get_object_or_404(questions, slug=self.kwargs['question'])
