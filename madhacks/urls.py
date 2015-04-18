from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'$', 'live.views.main_live'),
    url(r'^vote/', include('vote.urls')),
    url(r'^live/', include('live.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
