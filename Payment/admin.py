from django.contrib import admin

# Register your models here.
from .models import Payment,Subscription

admin.site.register(Payment)
admin.site.register(Subscription)