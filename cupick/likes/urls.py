from django.conf.urls import patterns, url

urlpatterns = patterns('cupick.likes.views',
    url(r'$', 'index', name='index'),
    # url(r'match/$', 'likes_match', name='likes_match'),
    # url(r'matched/$', 'likes_matched', name='likes_matched'),
    # url(r'liked/$', 'my_likes_list', name='my_likes_list'),
)
