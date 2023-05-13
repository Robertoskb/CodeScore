from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings

from exams.models import Exam, Question


class ExamMixin:

    def make_exam(self, name='Exam', avaliable=True):
        return Exam.objects.create(name=name, avaliable=avaliable)

    def make_question(self, name='Question', statement_pdf=None,
                      answer_zip=None, exam=None):

        return Question.objects.create(name=name,
                                       statement_pdf=statement_pdf or self.get_pdf(),  # noqa: E501
                                       answer_zip=answer_zip or self.get_zip(),
                                       exam=exam or self.make_exam())

    def make_exam_with_questions(self, qty=3):
        exam = self.make_exam()

        for i in range(qty):
            self.make_question(name=f'Question-{i+1}', exam=exam)

        return exam

    def get_pdf(self):
        return SimpleUploadedFile('statement.pdf', b'file_content',
                                  content_type='application/pdf')

    def get_zip(self):
        return SimpleUploadedFile('answer.zip', b'file_content',
                                  content_type='application/zip')


@override_settings(MEDIA_ROOT='/tmp')
class ExamTestBase(TestCase, ExamMixin):
    ...
