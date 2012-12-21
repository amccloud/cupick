import logging, urllib2, urlparse, geopy, facebook
from celery.task import task
from django.core.files.base import ContentFile
from django.contrib.gis.geos import Point
from django.contrib.gis.geoip import GeoIP
from cupick.profiles.models import User, UserPhoto

logger = logging.getLogger(__name__)

@task(ignore_result=True, rate_limit='30/m')
def geocode_user(user_id, location_name):
    try:
        gc = geopy.geocoders.GeoNames()
        location_name, location_latlng = gc.geocode(location_name, exactly_one=False)[0]
    except IndexError:
        return

    if ',' in location_name:
        location_name = location_name.split(',')[0]

    User.objects.filter(id=user_id).update(
        location_name=location_name,
        location_latlng=Point(*location_latlng))

@task(ignore_result=True)
def geolocate_user(user_id, ip=None):
    geo = GeoIP()
    results = geo.city(ip)

    User.objects.filter(id=user_id).update(
        location_country=results.get('country_code'),
        location_name=results.get('city'),
        location_latlng=geo.geos(ip))

@task(ignore_result=True)
def download_user_photo(url, **kwargs):
    name = urlparse.urlparse(url).path.split('/')[-1]
    content = ContentFile(urllib2.urlopen(url).read())
    user_photo = UserPhoto(**kwargs)
    user_photo.image.save(name, content, save=True)

@task(ignore_result=True)
def import_facebook_friends(uid, access_token, user_id=None):
    user = None

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist, e:
        logger.exception(e)

    graph = facebook.GraphAPI(access_token)
    results = graph.get_connections(uid, 'friends', fields='id,username,email,first_name,last_name,gender,location,birthday,interested_in,relationship_status,picture.width(1000)')

    for data in results['data']:
        friend = User()
        friend.load_facebook(**data)

        if user:
            user.friends.add(friend)
