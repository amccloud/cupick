from django.dispatch import receiver
from django.db.models.signals import post_save
from cupick.accounts.models import User
from cupick.credits.models import BillingProfile

@receiver(post_save, sender=User)
def create_billing_profile(sender, instance, created, **kwargs):
    if created:
        BillingProfile.objects.get_or_create(user=instance)
