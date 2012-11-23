from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url(r'^feeds/', include('feeds.urls')),
)
