from django.urls import resolve, reverse

from students import views

from .test_students_base import StudentTestBase


class StudentHomeViewTest(StudentTestBase):

    def test_students_home_view_function_is_correct(self):
        view = resolve(reverse('students:home'))

        self.assertIs(view.func.view_class, views.HomeView)

    def test_students_home_return_status_code_200(self):
        response = self.client.get(reverse('students:home'))

        self.assertIs(response.status_code, 200)

    def test_students_home_view_show_exams(self):
        exam = self.make_exam()

        response = self.client.get(reverse('students:home'))

        self.assertIn(exam.name, response.content.decode('utf-8'))
