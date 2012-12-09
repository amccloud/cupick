import urllib
from django.conf import settings

def _get_local_wan_ip():
    return urllib.urlopen('http://automation.whatismyip.com/n09230945.asp').read()

def get_ip(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR')

    if ip and ',' in ip:
        ip = ip.split(',')[0].strip()

    if not ip:
        ip = request.META.get('REMOTE_ADDR')

    if settings.DEBUG and ip == '127.0.0.1':
        ip = _get_local_wan_ip()

    return ip
