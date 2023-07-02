from django.urls import path

from . import views

app_name = 'students'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('prova/<str:exam>/', views.ExamView.as_view(), name='exam'),
    path('prova/<str:exam>/<str:question>',
         views.QuestionView.as_view(), name='question'),
    path('enunciado/<path:path>/',
         views.pdf_view, name='statement')
]
