from django import forms

from exams.models import Exam


class PINform(forms.Form):
    pin = forms.CharField(max_length=6, widget=forms.TextInput(attrs={
        'placeholder': 'PIN da prova'}))

    def clean_pin(self):
        pin = self.cleaned_data['pin'].upper()
        exam = Exam.objects.filter(code=pin, available=True).first()

        if not exam:
            raise forms.ValidationError('Prova não encontrada')

        return pin
