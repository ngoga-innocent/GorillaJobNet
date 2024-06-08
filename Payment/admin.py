from django.contrib import admin

# Register your models here.
from .models import Payment,Subscription,OTP

admin.site.register(Payment)
admin.site.register(Subscription)
admin.site.register(OTP)