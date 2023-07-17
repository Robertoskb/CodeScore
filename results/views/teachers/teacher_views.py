from django.views.generic import TemplateView

from results.models import Result, User
from teachers.views import TeacherMixin
from utils.get_exams import get_exam


def get_highest_scores(user, exam):
    highest_scores = {question.id: 0 for question in exam.questions.all()}

    results = Result.objects.filter(user=user, question__exam=exam)

    if not results:
        return None

    for submission in results.prefetch_related('question'):
        question_id = submission.question.id
        current_score = highest_scores[question_id]
        submission_score = submission.score_obtained

        if submission_score > current_score:
            highest_scores[question_id] = submission_score

    return highest_scores


def get_sum_of_highest_scores(user, exam):
    scores = get_highest_scores(user, exam)

    return sum(scores.values()) if scores is not None else scores


class ExamResultsView(TeacherMixin, TemplateView):
    template_name = 'results/pages/exam_results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        exam_name = kwargs['exam']

        exam = get_exam(exam_name)
        users = User.objects.all()

        users_score = ((user, get_sum_of_highest_scores(user, exam))
                       for user in users)

        context['users_score'] = users_score
        context['exam'] = exam

        return context
