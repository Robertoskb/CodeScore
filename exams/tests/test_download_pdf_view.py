from django.urls import reverse

from .test_exams_base import ExamTestBase


class ExamsDownloadViewTest(ExamTestBase):

    def test_exams_download_pdf_raises_404_if_path_not_found(self):
        response = self.client.get(
            reverse('exams:statement',
                    args=("enunciado/statements/file.pdf",)))

        self.assertEqual(404, response.status_code)

    def test_exams_download_view_returns_file(self):
        question = self.make_question()

        response = self.client.get(
            reverse('exams:statement', args=(question.statement_pdf.name,)))

        self.assertEqual(response['Content-Type'], 'application/pdf')
