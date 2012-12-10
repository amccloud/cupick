import logging, datetime, uuid
from django.contrib.gis.db import models
from django.utils.translation import ugettext as _
from dateutil.relativedelta import relativedelta
from easy_thumbnails.fields import ThumbnailerImageField
from cupick.common.choices import COUNTRY_CHOICES
from cupick.accounts.models import User
from cupick.profiles.managers import ApprovedProfileManager

logger = logging.getLogger(__name__)

def pick(value, options):
    return options.get(value, None)

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

    GUID_NAMESPACE = uuid.UUID('6ba7b815-9dad-11d1-80b4-00c04fd430c8')
    AGE_MIN = 18

    guid = models.CharField(max_length=64, unique=True, db_index=True, blank=True)
    user = models.OneToOneField(User, related_name='profile', blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=16, choices=GENDER_CHOICES, blank=True)
    orientation = models.CharField(max_length=16, choices=ORIENTATION_CHOICES, default=ORIENTATION_STRAIGHT, blank=True)
    location_country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, blank=True)
    location_name = models.CharField(max_length=255, blank=True)
    location_latlng = models.PointField(blank=True, null=True)

    objects = models.GeoManager()
    approved = ApprovedProfileManager()

    @property
    def name(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def age(self):
        if self.birthday:
            return relativedelta(datetime.date.today(), self.birthday).years

    @property
    def default_photo(self):
        return self.profile_photos.get(default=True)

    @property
    def default_photo_image(self):
        return self.default_photo.image

    def load_facebook(self, **kwargs):
        self.guid = uuid.uuid5(Profile.GUID_NAMESPACE, str('facebook:%(id)s' % kwargs))

        if 'first_name' in kwargs:
            self.first_name = kwargs['first_name']

        if 'last_name' in kwargs:
            self.last_name = kwargs['last_name']

        if 'gender' in kwargs:
            self.gender = pick(kwargs['gender'], {
                'male': Profile.GENDER_MALE,
                'female': Profile.GENDER_FEMALE,
            })

        if 'interested_in' in kwargs:
            if len(kwargs['interested_in']) > 1:
                self.orientation = Profile.ORIENTATION_BISEXUAL
            else:
                interested_in = pick(kwargs['interested_in'][0], {
                    'male': Profile.GENDER_MALE,
                    'female': Profile.GENDER_FEMALE,
                })

                if self.gender == interested_in:
                    self.orientation = Profile.ORIENTATION_GAY
                else:
                    self.orientation = Profile.ORIENTATION_STRAIGHT

        if 'birthday' in kwargs:
            try:
                # Example birthday: "06/22/1990"
                self.birthday = datetime.datetime.strptime(kwargs['birthday'], '%m/%d/%Y').date()
            except ValueError:
                logger.warning("Could not parse Facebook profile's birthday: '%s'" % kwargs['birthday'])

        if 'location' in kwargs and kwargs['location']['name']:
            self.location_name = kwargs['location']['name']

        if not self.id:
            self.save()

        if 'picture' in kwargs and not kwargs['picture']['data']['is_silhouette']:
            ProfilePhoto.from_url(kwargs['picture']['data']['url'], profile_id=self.id, approved=True)

    def save(self, *args, **kwargs):
        if not self.guid:
            self.guid = uuid.uuid5(Profile.GUID_NAMESPACE, str(uuid.uuid1()))

        super(Profile, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class ProfilePhoto(models.Model):
    profile = models.ForeignKey(Profile, related_name='profile_photos')
    image = ThumbnailerImageField(upload_to='profile-photos')
    caption = models.TextField(blank=True)
    default = models.BooleanField()
    approved = models.NullBooleanField()

    @classmethod
    def from_url(cls, url, **kwargs):
        from cupick.profiles.tasks import download_profile_photo
        download_profile_photo.delay(url, **kwargs)
