from django.urls import path
from .views import AdvertPostEdit,AdvertiserView,AnnouncementPostEdit, AnnouncementView,DeleteQuiz,duplicate_quiz_function,Home,Exam,get_All_faculty,QuestionView,get_Quiz,get_quiz_questions,Faculity,DeleteFaculity,DeleteQuestion,Get_Category_announcement
urlpatterns = [
    path('',Home,name='staff_home'),
    path('exam',Exam.as_view(),name='add_exam'),
    path('fetch_faculties',get_All_faculty,name='fetch_faculties'),
    path('add_questions',QuestionView.as_view(),name='questions'),
    path('get_quiz',get_Quiz,name='get_quiz'),
    path('get_quiz_questions',get_quiz_questions,name='get_questions'),
    path('delete_quiz',DeleteQuiz,name='delete_quiz'),
    path('faculity',Faculity.as_view(),name='faculity'),
    path('delete_fuculity',DeleteFaculity,name='delete-exam'),
    path('delete_question',DeleteQuestion,name='delete-question'),

    path('announcements',AnnouncementView.as_view(),name='staff_announcements'),
    path('announcement/detail/<uuid:id>',AnnouncementView.as_view(),name='staff_announcement_detail'),
    path('announcement/category/<uuid:id>',Get_Category_announcement,name='staff_announcement_category'),
    path('announcement/add_announcement',AnnouncementPostEdit.as_view(),name='staff_add_announcement'),
    path('product',AdvertiserView.as_view(),name='staff_products'),
    path('product/<uuid:id>',AdvertiserView.as_view(),name='staff_single_product'),
    path('addproduct',AdvertPostEdit.as_view(),name='staff_add_product'),
    path('editproduct/<uuid:id>',AdvertPostEdit.as_view(),name='staff_edit_product'),
    path('duplicate_quiz',duplicate_quiz_function,name='staff_duplicate_quiz'),
    
    
]