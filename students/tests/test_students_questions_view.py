from django.urls import resolve, reverse  # noqa: F401

from .test_students_base import StudentTestBase


class ExamsQuestionsViewTest(StudentTestBase):

    def test_students_questions_loads_correct_template(self):
        exam = self.make_exam()
        response = self.client.get(reverse('students:exam', args=(exam.slug,)))

        self.assertTemplateUsed(response, 'students/pages/questions.html')

    def test_students_questions_shows_questions(self):
        exam = self.make_exam_with_questions()

        response = self.client.get(reverse('students:exam', args=(exam.slug,)))
        content = response.content.decode('utf-8')

        for question in exam.questions.all():
            self.assertIn(question.name, content)

    def test_students_questions_raises_404_if_exam_does_not_exist(self):
        response = self.client.get(reverse('students:exam', args=('slug',)))

        self.assertEqual(response.status_code, 404)
