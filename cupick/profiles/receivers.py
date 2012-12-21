import logging
from django.dispatch import receiver
from django.db.models.signals import post_save
from social_auth.signals import pre_update
from social_auth.backends.facebook import FacebookBackend
from cupick.profiles.models import User, UserPhoto
from cupick.profiles.tasks import geocode_user, import_facebook_friends

logger = logging.getLogger(__name__)

@receiver(post_save, sender=UserPhoto)
def set_user_default_photo(sender, instance, created, **kwargs):
    if not instance.user.default_photo:
        instance.user.default_photo = instance
        instance.user.save()

@receiver(post_save, sender=User)
def guess_user_location_latlng(sender, instance, created, **kwargs):
    if not instance.location_latlng and instance.location_name:
        geocode_user.delay(instance.id, instance.location_name)

@receiver(pre_update, sender=FacebookBackend)
def import_user_friends(sender, user, response, details, **kwargs):
    for auth_profile in user.social_auth.filter(provider='facebook'):
        import_facebook_friends.delay(auth_profile.uid, auth_profile.tokens.get('access_token'), user.id)
