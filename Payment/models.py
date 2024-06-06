from django.db import models
import uuid
from django.contrib.auth.models import User
from Quiz.models import Quiz
from django.utils import timezone
# Create your models here.
class Payment(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    # paid_exam=models.ForeignKey(Quiz, on_delete=models.CASCADE)
    ref=models.CharField(max_length=255)
    valid=models.BooleanField(default=False)
    created_at=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} paid"
class Subscription(models.Model):
    choices=(
        ('day','Day'), ('week','Week'), ('Month','Month'),
    )
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    subscription_type=models.CharField(max_length=255,choices=choices)
    subscription_valid=models.BooleanField(default=False)
    end_date=models.DateField(null=True)

    def __str__(self):
        return f"{self.user.username} subscribed for {self.subscription_type}"


    