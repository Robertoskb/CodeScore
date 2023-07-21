from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from profiles.forms import LoginForm
from utils.user_type import get_user_type


def get_success_url(user):
    urls = {'admin': 'teachers:exams', 'teacher': 'teachers:exams'}
    user_type = get_user_type(user)

    return reverse_lazy(urls.get(user_type, 'students:search_pin'))


class LoginView(FormView):
    template_name = 'profiles/pages/login.html'
    form_class = LoginForm

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(get_success_url(self.request.user))
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )

        if user is not None:
            login(self.request, user)
            self.success_url = get_success_url(user)

        else:
            self.success_url = reverse_lazy('profiles:login')

        return super().form_valid(form)
