from django.conf.urls import patterns, include, url

urlpatterns =  patterns('interface.views',
    url(r'^$', 'interface_index', {}, name='interface_index'),
    url(r'^code/(?P<id>.+)/$', 'interface_view', {}, name='interface_view'),
    url(r'^sha1/$', 'sha1_view', {}, name='sha1_view'),
)