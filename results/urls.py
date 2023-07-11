from django.urls import path

from . import views

app_name = 'results'

urlpatterns = [
    path("prova/<str:exam>/", views.ExamResultsView.as_view(), name="exam"),
]
