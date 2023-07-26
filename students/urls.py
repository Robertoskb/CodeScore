from django.urls import path

from . import views

app_name = 'students'

urlpatterns = [
    path('', views.SearchPINView.as_view(), name='search_pin'),
    path('tutorial/', views.StudentTutorial.as_view(), name='tutorial'),
    path('prova/<str:pin>/', views.ExamView.as_view(), name='exam'),
    path('prova/<str:pin>/<str:question>',
         views.QuestionView.as_view(), name='question'),
    path('enunciado/<str:question>/<path:path>/',
         views.pdf_view, name='statement')
]
