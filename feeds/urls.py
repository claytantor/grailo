from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    (r'index.html', 'feeds.views.index'),
    (r'home.html', 'feeds.views.home'),
    (r'login.html', 'feeds.views.login_user'),
    (r'logout.html', 'feeds.views.logout_user'),
    (r'register.html', 'feeds.views.register'),
    (r'uname.json', 'feeds.views.uname_json'),
)
