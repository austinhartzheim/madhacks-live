from django.conf.urls import patterns, url

urlpatterns = patterns('live.views',
    url('^fetch/$', 'fetch'),
    url('^$', 'main_live')
)
