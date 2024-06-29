from django.urls import path
from .views import AnnouncementView,CheckOtp,CheckPaymentStatus,get_announcement_detail,search_announcement,CheckUserAnnouncement,payAnnouncement
urlpatterns = [
    path('',AnnouncementView.as_view(),name='announcements'),
    path('<uuid:id>',AnnouncementView.as_view(),name='announcements_categories'),
    path('detail/<uuid:announcement_id>',get_announcement_detail,name='announcement_detail'),
    path('search/<str:text>',search_announcement,name='announcement_search'),
    path('check_ann',CheckUserAnnouncement,name='check_announcement'),
    path('pay_announc',payAnnouncement,name='pay_announcement'),
    path('check_announc_paid',CheckPaymentStatus,name='check_announcement_paid'),
    path('check_otp',CheckOtp,name='check_otp'),
]