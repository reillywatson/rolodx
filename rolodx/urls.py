from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.home'),
    url(r'^category/(?P<category_name>.+)/$', 'main.views.category'), #direct category access
    url(r'^search/',  'main.views.search'),
    url(r'^pro/(?P<itemId>\d+)/addReview$', 'main.views.addReview'),
    url(r'^pro/(?P<itemId>\d+/?$)', 'main.views.item'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^social/', include('socialregistration.urls', namespace = 'socialregistration')),
)

urlpatterns += staticfiles_urlpatterns()
