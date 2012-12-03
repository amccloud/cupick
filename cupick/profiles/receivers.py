import logging, datetime
from django.dispatch import receiver
from django.db.models.signals import post_save
from social_auth.signals import pre_update
from social_auth.backends.facebook import FacebookBackend
from cupick.accounts.models import User
from cupick.profiles.models import Profile

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(pre_update, sender=FacebookBackend)
def sync_profile_from_facebook(sender, user, response, details, **kwargs):
    if not bool(user.profile.gender):
        setattr(user.profile.gender, response.get('gender'), True)

    if hasattr(response, 'birthday'):
        try:
            # Example birthday: 06/22/1990
            user.profile.birthday = datetime.datetime.strptime(response.get('birthday'), '%m/%d/%Y').date()
        except ValueError:
            logger.exception("Could not parse Facebook profile's birthday:")

    user.profile.save()
