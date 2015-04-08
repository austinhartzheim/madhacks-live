from django.conf.urls import patterns, url

urlpatterns = patterns('vote.views',
    url('^enter/$', 'vote_enter_prompt'),
    url('^enter/submit$', 'vote_enter_submit'),
    url('^submit$', 'vote_submit'),
)
