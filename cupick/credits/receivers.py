from django.dispatch import receiver
from django.db.models.signals import post_save
from cupick.profiles.models import Profile
from cupick.credits.models import ProfileBilling

@receiver(post_save, sender=Profile)
def create_billing_profile(sender, instance, created, **kwargs):
    if created:
        ProfileBilling.objects.get_or_create(Profile=instance)
