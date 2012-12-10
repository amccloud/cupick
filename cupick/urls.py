from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/', include('debug_toolbar_user_panel.urls')),
    # url(r'^account/', include('registration.urls')),
    url(r'^account/', include('social_auth.urls')),
    url(r'^profiles/', include('cupick.profiles.urls')),
    url(r'^credits/', include('cupick.credits.urls')),
    url(r'^$', TemplateView.as_view(template_name='index.html')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^public/media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
   )
