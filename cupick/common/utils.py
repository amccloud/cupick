import copy, urllib
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule
from django.contrib.admin.sites import site

def autodiscover(name):
    for app in settings.INSTALLED_APPS:
        mod = import_module(app)

        try:
            before_import_registry = copy.copy(site._registry)
            import_module('%s.%s' % (app, name))
        except:
            site._registry = before_import_registry

            if module_has_submodule(mod, name):
                raise

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
