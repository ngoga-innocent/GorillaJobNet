from django.urls import path
from .views import Home,Exam,get_All_faculty,QuestionView,get_Quiz,get_quiz_questions,Faculity,DeleteFaculity
urlpatterns = [
    path('',Home,name='staff_home'),
    path('exam',Exam.as_view(),name='add_exam'),
    path('fetch_faculties',get_All_faculty,name='fetch_faculties'),
    path('add_questions',QuestionView.as_view(),name='questions'),
    path('get_quiz',get_Quiz,name='get_quiz'),
    path('get_quiz_questions',get_quiz_questions,name='get_questions'),
    
    path('faculity',Faculity.as_view(),name='faculity'),
    path('delete-fuculity',DeleteFaculity,name='delete-exam'),

    
    
]