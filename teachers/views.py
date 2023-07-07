from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView, UpdateView

from exams.forms import Exam, ExamForm, Question, QuestionForm
from utils.get_exams import get_exam, get_object_or_404
from django.core.exceptions import PermissionDenied
from utils.sidebar_mixin import SideBarMixin, get_user_type


class TeacherMixin(SideBarMixin, object):
    def get(self, *args, **kwargs):
        user_type = get_user_type(self.request.user)

        if 'admin' != user_type != 'teacher':
            raise PermissionDenied

        return super(TeacherMixin, self).get(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(TeacherMixin, self).get_context_data(**kwargs)

        user_type = get_user_type(self.request.user)

        context["teacher_permision"] = not ('admin' != user_type != 'teacher')

        return context


class TeacherExams(TeacherMixin, TemplateView):
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
        exam = get_exam(self.kwargs['exam'])

        question = form.save(commit=False)
        question.exam = exam
        question.save()

        self.success_url = reverse('teachers:exam', args=(exam.slug,))

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['exam'] = get_exam(self.kwargs['exam'])

        return context


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
