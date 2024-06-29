from django.db import models
import uuid
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
# Create your models here.
class AnnouncementCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.name}"
    def get_category_annoucement(self):
        return self.announcement_set.all()
    class Meta:
        verbose_name = "Announcement Category"
        verbose_name_plural = "Announcement Categories"
class Announcement(models.Model):

    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    category=models.ForeignKey(AnnouncementCategory,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    slug=models.CharField(max_length=255,null=True,blank=True)
    thumbnail=models.ImageField(upload_to='Announcements/thumbnails',null=True)
    description=RichTextField()
    application_link=models.URLField(max_length=255,null=True,blank=True)
    company_name=models.CharField(max_length=255)
    announcer=models.ForeignKey(User, on_delete=models.CASCADE)
    deadline=models.DateTimeField(null=True, blank=True)
    location=models.CharField(max_length=255,null=True, blank=True)
    experience=models.CharField(max_length=255,null=True, blank=True)
    announcer_description=RichTextField(null=True, blank=True)
    announcer_logo=models.ImageField(upload_to='Announcements/announcer_logos',null=True,blank=True)
    valid=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.title} {self.announcer}"
class Paid_Announcencer(models.Model):
    announcer=models.ForeignKey(User, on_delete=models.CASCADE)
    otp=models.CharField(max_length=10)
    paid=models.BooleanField(default=False)
    valid=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.announcer}"    