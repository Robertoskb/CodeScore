from django.urls import resolve, reverse  # noqa: F401

from .test_exams_base import ExamTestBase


class ExamsQuestionsViewTest(ExamTestBase):

    def test_exams_questions_loads_correct_template(self):
        exam = self.make_exam()
        response = self.client.get(reverse('exams:exam', args=(exam.slug,)))

        self.assertTemplateUsed(response, 'exams/pages/questions.html')

    def test_exams_questions_shows_questions(self):
        exam = self.make_exam_with_questions()

        response = self.client.get(reverse('exams:exam', args=(exam.slug,)))
        content = response.content.decode('utf-8')

        for question in exam.questions.all():
            self.assertIn(question.name, content)

    def test_exams_questions_raises_404_if_exam_does_not_exist(self):
        response = self.client.get(reverse('exams:exam', args=('slug',)))

        self.assertEqual(response.status_code, 404)
