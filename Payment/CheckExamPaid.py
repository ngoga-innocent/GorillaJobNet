from Payment.models import Payment,Subscription,OTP
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from Quiz.models import Quiz

def CheckUserPayment(user,otp):
    user = get_object_or_404(User,pk=user)
    OTP=get_object_or_404(Quiz,pk=otp)
    try:
        
        payment=Payment.objects.filter(user=user,otp=OTP).first()
        if payment and payment.valid:
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
def CheckOTP(otp):
    try:
        otp=OTP.objects.get(otp=otp)
        if otp.valid:
            if otp.type !='one' and timezone.now() >=otp.end_validated_date:
                otp.valid=False
                otp.save()
                return False
            return True
        return False
        
    except OTP.DoesNotExist:
        return False