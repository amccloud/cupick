import logging
from django.dispatch import receiver
from django.db.models.signals import post_save
from social_auth.signals import pre_update
from social_auth.backends.facebook import FacebookBackend
from cupick.accounts.models import User
from cupick.profiles.models import Profile
from cupick.profiles.tasks import geocode_profile, import_facebook_friends

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance, defaults={
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
        })

@receiver(post_save, sender=Profile)
def guess_profile_location_latlng(sender, instance, created, **kwargs):
    if not instance.location_latlng and instance.location_name:
        geocode_profile.delay(instance.id, instance.location_name)

@receiver(pre_update, sender=FacebookBackend)
def import_profiles_friends(sender, user, response, details, **kwargs):
    for auth_profile in user.social_auth.filter(provider='facebook'):
        import_facebook_friends.delay(auth_profile.uid, auth_profile.tokens.get('access_token'))
