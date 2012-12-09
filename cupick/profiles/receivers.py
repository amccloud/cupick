import logging
from django.dispatch import receiver
from django.db.models.signals import post_save
from cupick.accounts.models import User
from cupick.profiles.models import Profile
from cupick.profiles.tasks import geocode_profile

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=Profile)
def guess_profile_location_latlng(sender, instance, created, **kwargs):
    if not instance.location_latlng and instance.location_name:
        # TODO: delay
        geocode_profile(instance.id, instance.location_name)
