import logging, datetime, uuid
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext as _
from dateutil.relativedelta import relativedelta
from easy_thumbnails.fields import ThumbnailerImageField
from cupick.common.choices import COUNTRY_CHOICES
from cupick.profiles.managers import UserManager, ApprovedUserManager

logger = logging.getLogger(__name__)

def pick(value, options):
    return options.get(value, None)

class User(AbstractUser):
    GENDER_MALE = 'male'
    GENDER_FEMALE = 'female'
    GENDER_CHOICES = (
        (GENDER_MALE, _('Male')),
        (GENDER_FEMALE, _('Female')),
    )

    ORIENTATION_STRAIGHT = 'straight'
    ORIENTATION_BISEXUAL = 'bisexual'
    ORIENTATION_GAY = 'gay'
    ORIENTATION_CHOICES = (
        (ORIENTATION_STRAIGHT, _('Straight')),
        (ORIENTATION_BISEXUAL, _('Bisexual')),
        (ORIENTATION_GAY, _('Gay')),
    )

    GUID_NAMESPACE = uuid.UUID('6ba7b815-9dad-11d1-80b4-00c04fd430c8')
    AGE_MIN = 18

    guid = models.CharField(max_length=64, unique=True, db_index=True, blank=True)
    default_photo = models.ForeignKey('UserPhoto', related_name='+', blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=16, choices=GENDER_CHOICES, blank=True)
    orientation = models.CharField(max_length=16, choices=ORIENTATION_CHOICES, default=ORIENTATION_STRAIGHT, blank=True)
    location_country = models.CharField(max_length=2, choices=COUNTRY_CHOICES, blank=True)
    location_name = models.CharField(max_length=255, blank=True)
    location_latlng = models.PointField(blank=True, null=True)
    friends = models.ManyToManyField('self', related_name='+', blank=True)

    objects = UserManager()
    approved = ApprovedUserManager()

    @property
    def name(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def age(self):
        if self.birthday:
            return relativedelta(datetime.date.today(), self.birthday).years

    @property
    def default_photo_image(self):
        if self.default_photo:
            return self.default_photo.image

    def load_facebook(self, **kwargs):
        self.guid = uuid.uuid5(User.GUID_NAMESPACE, str('facebook:%(id)s' % kwargs))

        if 'username' in kwargs:
            self.username = kwargs['username']

        if 'first_name' in kwargs:
            self.first_name = kwargs['first_name']

        if 'last_name' in kwargs:
            self.last_name = kwargs['last_name']

        if 'email' in kwargs:
            self.email = kwargs['email']

        if 'gender' in kwargs:
            self.gender = pick(kwargs['gender'], {
                'male': User.GENDER_MALE,
                'female': User.GENDER_FEMALE,
            })

        if 'interested_in' in kwargs:
            if len(kwargs['interested_in']) > 1:
                self.orientation = User.ORIENTATION_BISEXUAL
            else:
                interested_in = pick(kwargs['interested_in'][0], {
                    'male': User.GENDER_MALE,
                    'female': User.GENDER_FEMALE,
                })

                if self.gender == interested_in:
                    self.orientation = User.ORIENTATION_GAY
                else:
                    self.orientation = User.ORIENTATION_STRAIGHT

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
            UserPhoto.from_url(kwargs['picture']['data']['url'], user_id=self.id, approved=True)

    def save(self, *args, **kwargs):
        if not self.guid:
            self.guid = uuid.uuid5(User.GUID_NAMESPACE, str(uuid.uuid1()))

        super(User, self).save(*args, **kwargs)

class UserPhoto(models.Model):
    user = models.ForeignKey(User, related_name='photos')
    image = ThumbnailerImageField(upload_to='user-photos')
    caption = models.TextField(blank=True)
    approved = models.NullBooleanField()

    @classmethod
    def from_url(cls, url, **kwargs):
        from cupick.profiles.tasks import download_user_photo
        download_user_photo.delay(url, **kwargs)

    def __unicode__(self):
        return self.image.name
