# import magic
from django import forms

from .models import Exam, Question


class PythonFileForm(forms.Form):
    python_file = forms.FileField(label='Arquivo Python:')

    def clean_python_file(self):
        file = self.cleaned_data['python_file']

        if not file.name.endswith('.py'):
            raise forms.ValidationError('Submeta um arquivo python válio!')

        return file


class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['name']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['name', 'statement_pdf', 'answer_zip']
