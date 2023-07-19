from django.urls import path

from . import views

app_name = 'teachers'

urlpatterns = [
    path('', views.TeacherExams.as_view(),  name='exams'),
    path("prova/criar", views.CreateExam.as_view(), name="create_exam"),
    path('prova/<str:exam>/', views.TeacherQuestions.as_view(), name='exam'),
    path("prova/<str:exam>/criar/",
         views.CreateQuestion.as_view(), name="create_question"),
    path("prova/<str:exam>/editar/",
         views.UpdateExam.as_view(), name="update_exam"),
    path("prova/<str:exam>/<str:question>/editar/",
         views.UpdateQuestion.as_view(), name="update_question"),
]
