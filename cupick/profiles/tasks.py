import logging
from celery.task import task
from geopy import geocoders
from django.contrib.gis.geos import Point
from django.contrib.gis.geoip import GeoIP
from cupick.profiles.models import Profile

logger = logging.getLogger(__name__)

@task
def geocode_profile(profile_id, location_name):
    try:
        gc = geocoders.GeoNames()
        location_name, location_latlng = gc.geocode(location_name, exactly_one=False)[0]
    except IndexError:
        return

    if ',' in location_name:
        location_name = ','.join(location_name.split(',')[:2])

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
