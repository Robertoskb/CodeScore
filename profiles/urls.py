from django.urls import path

from . import views

app_name = 'profiles'

urlpatterns = [
    path("", views.LoginView.as_view(), name="login"),
]
