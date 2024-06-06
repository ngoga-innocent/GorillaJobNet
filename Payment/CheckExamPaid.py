from Payment.models import Payment,Subscription
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def CheckUserPayment(user):
    user = get_object_or_404(User,pk=user)
    try:
        
        payment=Payment.objects.get(user=user)
        if payment.valid:
            return True
        return False
        
    except Payment.DoesNotExist:
        return False    
   
def CheckUserSubscription(user):
    user = get_object_or_404(User,pk=user)
    try:
        
        subscription=Subscription.objects.get(user=user)
        if timezone.now() >= subscription.end_date:
            subscription.valid=False
            subscription.save()
            return False

        else:
            return True
        
    except Subscription.DoesNotExist:
        return False