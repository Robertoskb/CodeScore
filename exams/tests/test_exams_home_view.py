from django.urls import resolve, reverse

from exams import views

from .test_exams_base import ExamTestBase


class ExamsHomeViewTest(ExamTestBase):

    def test_exams_home_view_function_is_correct(self):
        view = resolve(reverse('exams:home'))

        self.assertIs(view.func.view_class, views.HomeView)

    def test_exams_home_return_status_code_200(self):
        response = self.client.get(reverse('exams:home'))

        self.assertIs(response.status_code, 200)

    def test_exams_home_view_show_exams(self):
        exam = self.make_exam()

        response = self.client.get(reverse('exams:home'))

        self.assertIn(exam.name, response.content.decode('utf-8'))
