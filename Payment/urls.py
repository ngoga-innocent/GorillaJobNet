from django.urls import path
from .views import PaymentView,Webhook,CheckPaymentStatus
urlpatterns = [
    path('',PaymentView.as_view(),name='payment'),
    path("checkWebHook",Webhook,name='checkwebhook'),
    path("payment_status",CheckPaymentStatus,name='payment_status')
]