from django.contrib.gis.db import models
from django.utils.translation import ugettext as _
from easy_thumbnails.fields import ThumbnailerImageField
from cupick.common.choices import COUNTRY_CHOICES
from cupick.accounts.models import User

class Profile(models.Model):
    GENDER_MALE = 'male'
    GENDER_FEMALE = 'female'
    GENDER_CHOICES = (
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
    )

    ORIENTATION_STRAIGHT = 'straight'
    ORIENTATION_BISEXUAL = 'bisexual'
    ORIENTATION_GAY = 'gay'
    ORIENTATION_CHOICES = (
        (ORIENTATION_STRAIGHT, _("Straight")),
        (ORIENTATION_BISEXUAL, _("Bisexual")),
        (ORIENTATION_GAY, _("Gay")),
    )

    user = models.OneToOneField(User, related_name='profile', blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=16, choices=GENDER_CHOICES, blank=True)
    orientation = models.CharField(max_length=16, choices=ORIENTATION_CHOICES, blank=True)
    location_country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, blank=True)
    location_name = models.CharField(max_length=255, blank=True)
    location_latlng = models.PointField(blank=True, null=True)

    objects = models.GeoManager()

    def __unicode__(self):
        return unicode(self.user)

class ProfilePhoto(models.Model):
    profile = models.ForeignKey(Profile, related_name='photos')
    image = ThumbnailerImageField(upload_to='profile-photos')
    caption = models.TextField(blank=True)
    default = models.BooleanField()
    approved = models.NullBooleanField()

from cupick.profiles.receivers import *
