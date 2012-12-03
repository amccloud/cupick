from django.conf.urls import patterns, url

urlpatterns = patterns('cupick.profiles.views',
    url(r'^search/$', 'profile_search', name='profile_search'),
    url(r'^match/$', 'profile_matches', name='profile_matches'),
    url(r'^(?P<username>[\w]+)/$', 'profile_detail', name='profile_detail'),
)
