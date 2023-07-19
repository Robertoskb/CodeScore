from results.models import Result


def get_exam_results_from_user(user, exam):
    questions = {question.name: {'submissions': [], 'score': 0}
                 for question in exam.questions.all()}

    results = Result.objects.filter(user=user, question__exam=exam)

    for submission in results.prefetch_related('question'):
        question_name = submission.question.name
        questions[question_name]['submissions'].append(submission)

        current_score = questions[question_name]['score']
        submission_score = submission.score_obtained

        if submission_score > current_score:
            questions[question_name]['score'] = submission_score

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
