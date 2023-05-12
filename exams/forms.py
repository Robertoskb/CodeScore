from django import forms

from .models import Exam, Question


class PythonFileForm(forms.Form):
    python_file = forms.FileField(label='Arquivo Python')


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['name', 'statement_pdf', 'answer_zip']
