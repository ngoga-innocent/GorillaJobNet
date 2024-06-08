
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('exam/',include('Quiz.urls'),name='exam'),
    path('',include('Home.urls'),name='home'),
    path('account/',include('Login.urls'),name='account'),
    path('payment/',include('Payment.urls'),name='payment'),
    path('staff/',include('Staff.urls'),name='staff'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
