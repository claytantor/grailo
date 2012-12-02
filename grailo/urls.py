from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('',
    #url(r'^$', direct_to_template, {'template': 'index.html'}),
    #url(r'^index.html', direct_to_template, {'template': 'index.html'}),
    #url(r'^feeds/', include('feeds.urls')),

    url(r'^$', 'feeds.views.index',name='site_landing'),
    url(r'^index.html', 'feeds.views.index',name='site_landing'),
    url(r'^home.html', 'feeds.views.home', name='templar_home'),
    url(r'^login.html', 'feeds.views.login_user', name='login'),
    url(r'^logout.html', 'feeds.views.logout_user', name='logout'),
    url(r'^register.html', 'feeds.views.register', name='register'),
    url(r'^feeds.html', 'feeds.views.templar_feeds', name='templar_feeds'),
    url(r'^about.html', TemplateView.as_view(
        template_name='about.html',
    )),


    #id based views
    url(r'^feed/(\w+)/$', 'feeds.views.feed', name='feed'),
    url(r'^profile/(\w+)/$', 'feeds.views.profile_detail', name='profile_detail'),
    url(r'^message/(\w+)/$', 'feeds.views.message', name='message'),
    url(r'^reply/(\w+)/$', 'feeds.views.reply_message', name='reply_message'),
    url(r'^delete/(\w+)/$', 'feeds.views.delete_message', name='delete_message'),

    #user image
    url(r'^avatar/(\w+).png', 'feeds.views.avatar_png', name='avatar'),

    #json api
    url(r'^follow/(\w+).json', 'feeds.views.follow_feed', name='follow_feed'),
    url(r'^uname.json', 'feeds.views.uname_json'),
)
