from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls),name='feeds_admin'),

    #url(r'^(?i)faqs/$', direct_to_template, {'template': 'main/faqs.html'}, name="main_faqs"),

    url(r'^$', 'feeds.views.index',name='site_landing'),
    url(r'^index.html', 'feeds.views.index',name='site_landing'),
    url(r'^home.html', 'feeds.views.home', name='templar_home'),
    url(r'^login.html', 'feeds.views.login_user', name='login'),
    url(r'^logout.html', 'feeds.views.logout_user', name='logout'),
    url(r'^register.html', 'feeds.views.register', name='register'),
    url(r'^feeds.html', 'feeds.views.templar_feeds', name='templar_feeds'),

    #id based views
    url(r'^feed/(\w+)/$', 'feeds.views.feed', name='feed'),
    url(r'^profile/(\w+)/$', 'feeds.views.profile_detail', name='profile_detail'),
    url(r'^message/(\w+)/$', 'feeds.views.message', name='message'),
    url(r'^reply/(\w+)/$', 'feeds.views.reply_message', name='reply_message'),

    #user image
    url(r'^avatar/(\w+).png', 'feeds.views.avatar_png', name='avatar'),

    #json api
    url(r'^follow/(\w+).json', 'feeds.views.follow_feed', name='follow_feed'),
    url(r'^uname.json', 'feeds.views.uname_json'),



#    url(r'^personal.html', 'feeds.views.personal', name='messages_you_follow'),
#    url(r'^all.html', 'feeds.views.public', name='all_messages'),
#    url(r'^(\d+)/$', 'feeds.views.single', name='single_message'),
#    url(r'^followers/(\w+)/$', 'feeds.views.followers', name='message_followers'),
#    url(r'^following/(\w+)/$', 'feeds.views.following', name='message_following'),
#    url(r'^toggle_follow/(\w+)/$', 'feeds.views.toggle_follow', name='toggle_follow'),


)

