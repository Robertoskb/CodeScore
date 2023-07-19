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

        labels = {
            'name': 'Nome da Prova'
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ex: Primeira Avaliação'
            }),
        }

        fields = ['name']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        labels = {
            'name': 'Nome da Questão:',
            'statement_pdf': 'Enunciado em PDF:',
            'answer_zip': 'Gabarito em ZIP:',
        }

        fields = ['name', 'statement_pdf', 'answer_zip']

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Ex: Menor Caminho'
            }),
        }
