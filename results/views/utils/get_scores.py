from django.http import Http404

from results.models import Result


def get_questions_maximum_score(user, question):
    result = Result.objects.filter(
        user=user, question=question,
        need_resubmission=False).order_by('-score_obtained').first()

    return result


def get_exam_results_from_user(user, exam):
    questions = {question.name: {'submissions': [],
                                 'scores': {
                                     'score_obtained': 0,
                                     'max_score': question.max_score}}
                 for question in exam.questions.all()}

    results = Result.objects.filter(
        user=user, question__exam=exam).order_by('-id')

    if not results:
        raise Http404()

    for submission in results.prefetch_related('question'):
        question_name = submission.question.name
        questions[question_name]['submissions'].append(submission)

        current_score = questions[question_name]['scores']['score_obtained']
        submission_score = submission.score_obtained
        need_resubmission = submission.need_resubmission

        if submission_score > current_score and not need_resubmission:
            questions[question_name]['scores']['score_obtained'] = submission_score  # noqa:E501

    return questions


def get_highest_scores(user, exam):
    results = Result.objects.filter(user=user, question__exam=exam)

    if not results:
        return None

    highest_scores = {question.id: 0 for question in exam.questions.all()}

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
