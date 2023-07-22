from django.urls import path

from . import views

app_name = 'results'

urlpatterns = [
    path("prova/<str:exam>/", views.ExamResultsView.as_view(), name="exam"),
    path("<str:username>/", views.ResultsStudentOverView.as_view(), name="exams"),  # noqa:E501
    path("prova/<str:exam>/<str:username>/", views.ResultsStudentView.as_view(), name="user"),  # noqa:E501
    path("download/<int:id>/<path:path>/",
         views.python_download_view, name="solution")
]
