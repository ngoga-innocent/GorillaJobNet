from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Payment, Subscription,OTP
import logging
from django.utils import timezone

# Get an instance of a logger
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Payment)
def payment_saved(sender, instance, created, **kwargs):
    if created:
        # Payment was just created
        logger.info(f'Payment created: {instance.ref}')
    else:
        # Payment was updated
        if instance.type != 'one' and instance.valid:
            # Ensure all required fields for Subscription are provided
            subscription = Subscription.objects.create(
                user=instance.user,
                subscription_type=instance.type,
                subscription_valid=True
            )
            logger.info(f'Subscription created: {subscription.id} for user {instance.user}')
        logger.info(f'Payment updated: {instance.ref} {instance.type}')
@receiver(post_save, sender=Subscription)        
def subscription_end_date(sender,instance,created,**kwargs):
    if created:
        if instance.subscription_type =='day':
            instance.end_date = timezone.now() + timezone.timedelta(days=1)
            instance.save(update_fields=['end_date']) 
        elif instance.subscription_type =='week':
            instance.end_date = timezone.now() + timezone.timedelta(weeks=1)
            instance.save(update_fields=['end_date'])
        elif instance.subscription_type =='month':
            instance.end_date = timezone.now() + timezone.timedelta(weeks=4)
            instance.save(update_fields=['end_date'])   

@receiver(post_save, sender=OTP)        
def Otp_end_date(sender,instance,created,**kwargs):
    if created:
        if instance.type =='day':
            instance.end_date = timezone.now() + timezone.timedelta(days=1)
            instance.save(update_fields=['end_validated_date']) 
        elif instance.type =='week':
            instance.end_date = timezone.now() + timezone.timedelta(weeks=1)
            instance.save(update_fields=['end_validated_date'])
        elif instance.type =='month':
            instance.end_date = timezone.now() + timezone.timedelta(weeks=4)
            instance.save(update_fields=['end_validated_date'])                     
    

