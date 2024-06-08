from django.db import models
import uuid
from django.contrib.auth.models import User
# from Quiz.models import Quiz
from django.utils import timezone
# Create your models here.
choices=(
        ('day','Day'), ('week','Week'), ('month','Month'),('one',"One")
    )
class OTP(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    otp=models.CharField(max_length=255)
    valid=models.BooleanField(default=False)
    type=models.CharField(max_length=14,choices=choices,default='one')
    created_at=models.DateTimeField(default=timezone.now)
    end_validated_date=models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.otp}"  
class Payment(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    otp=models.ForeignKey(OTP, on_delete=models.CASCADE,null=True)
    ref=models.CharField(max_length=255)
    valid=models.BooleanField(default=False)
    created_at=models.DateTimeField(default=timezone.now)
    type=models.CharField(max_length=255,choices=choices,default='one')
    def __str__(self):
        return f"{self.id} paid"
class Subscription(models.Model):
    
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    subscription_type=models.CharField(max_length=255,choices=choices)
    subscription_valid=models.BooleanField(default=False)
    end_date=models.DateField(null=True)
    otp=models.ForeignKey(OTP,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return f"{self.user.username} subscribed for {self.subscription_type}"
  

    