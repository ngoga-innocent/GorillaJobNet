
from django.contrib import admin
from django.urls import path,include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
urlpatterns = [
    path('admin/', admin.site.urls),
    path('exam/',include('Quiz.urls'),name='exam'),
    path('',include('Home.urls'),name='home'),
    path('account/',include('Login.urls'),name='account'),
    path('payment/',include('Payment.urls'),name='payment'),
    path('staff/',include('Staff.urls'),name='staff'),
    path('announcements/',include('Announcement.urls'),name='announcements'),
    path('esoko/',include('ESOKO.urls'),name='esoko'),
    #Browser Reloading
    path("__reload__/", include("django_browser_reload.urls")),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
