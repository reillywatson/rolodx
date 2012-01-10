from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.home'),
    url(r'^onecolumnbase$', 'main.views.base'),
    url(r'^category/(?P<category_name>.+)/$', 'main.views.category'), #direct category access
    url(r'^search$', 'main.views.search_category'), #searching with POST
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
