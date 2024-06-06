
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('exam/',include('Quiz.urls'),name='exam'),
    path('',include('Home.urls'),name='home'),
    path('account/',include('Login.urls'),name='account'),
    path('payment/',include('Payment.urls'),name='payment'),
]
