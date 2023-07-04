from django.views.generic import FormView
from profiles.forms import LoginForm
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate


class LoginView(FormView):
    template_name = 'profiles/pages/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )

        if user is not None:
            login(self.request, user)
            self.success_url = reverse_lazy('students:home')
        else:
            self.success_url = reverse_lazy('profiles:login')

        return super().form_valid(form)
