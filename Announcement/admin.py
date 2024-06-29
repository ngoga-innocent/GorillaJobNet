from django.contrib import admin

# Register your models here.
from .models import Announcement, AnnouncementCategory,Paid_Announcencer
admin.site.register(AnnouncementCategory)
admin.site.register(Announcement)
admin.site.register(Paid_Announcencer)