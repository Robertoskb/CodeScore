from django.urls import path

from . import views

app_name = 'results'

urlpatterns = [
    path("prova/<str:exam>/", views.ExamResultsView.as_view(), name="exam"),
    path("prova/<str:exam>/aluno", views.ResultsStudentView.as_view(), name="user")  # noqa:E501
]
