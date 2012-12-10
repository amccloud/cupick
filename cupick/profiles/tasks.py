import logging, urllib2, urlparse, geopy, facebook
from django.db import IntegrityError
from celery.task import task
from django.core.files.base import ContentFile
from django.contrib.gis.geos import Point
from django.contrib.gis.geoip import GeoIP
from cupick.profiles.models import Profile, ProfilePhoto

logger = logging.getLogger(__name__)

@task(rate_limit='30/m')
def geocode_profile(profile_id, location_name):
    try:
        gc = geopy.geocoders.GeoNames()
        location_name, location_latlng = gc.geocode(location_name, exactly_one=False)[0]
    except IndexError:
        return

    if ',' in location_name:
        location_name = location_name.split(',')[0]

    Profile.objects.filter(id=profile_id).update(
        location_name=location_name,
        location_latlng=Point(*location_latlng))

@task
def geolocate_profile(profile_id, ip=None):
    geo = GeoIP()
    results = geo.city(ip)

    Profile.objects.filter(id=profile_id).update(
        location_country=results.get('country_code'),
        location_name=results.get('city'),
        location_latlng=geo.geos(ip))

@task
def download_profile_photo(url, **kwargs):
    name = urlparse.urlparse(url).path.split('/')[-1]
    content = ContentFile(urllib2.urlopen(url).read())
    profile_photo = ProfilePhoto(**kwargs)
    profile_photo.image.save(name, content, save=True)

@task
def import_facebook_friends(uid, access_token):
    graph = facebook.GraphAPI(access_token)
    results = graph.get_connections(uid, 'friends', fields='id,first_name,last_name,gender,location,birthday,interested_in,relationship_status,picture.width(1000)')

    for friend in results['data']:
        profile = Profile()

        try:
            profile.load_facebook(**friend)
        except IntegrityError:
            logger.info("Skipping friend, profile %s already exist." % (profile.guid))
