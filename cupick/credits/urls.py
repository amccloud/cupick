from django.conf.urls import patterns, url

urlpatterns = patterns('cupick.credits.views',
    url(r'^buy/$', 'buy_credits', name='buy_credits'),
    url(r'^billing/$', 'billing_profile_update', name='billing_profile_update'),
)
