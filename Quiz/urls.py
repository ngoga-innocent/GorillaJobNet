from django.urls import path
from .views import quizHome,FaculityQuizes,QuizQuestions,SubmitUserResponse,GetAnswer,GetAllAnswer,CheckUserPaidExam,verifyCode,get_csrf_token
urlpatterns = [
    path('',quizHome,name='quiz_home'),
    path("<uuid:pk>",FaculityQuizes,name='faculty_quizes'),
    path("exam/<uuid:pk>",QuizQuestions,name='quiz_questions'),
    path("submit",SubmitUserResponse,name='submit_answers'),
    path("get_results/<uuid:id>",GetAnswer,name='get_answers'),
    path("get_all_answer",GetAllAnswer,name='get_all_answer'),
    path("Checkpayment",CheckUserPaidExam,name='checkpayment'),
    path("check_otp",verifyCode,name='check_otp'),
     path('csrf_token/', get_csrf_token, name='get_csrf_token'),
    
]