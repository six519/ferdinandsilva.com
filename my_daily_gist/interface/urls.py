from django.conf.urls import patterns, include, url

urlpatterns =  patterns('interface.views',
    url(r'^$', 'interface_index', {}, name='interface_index'),
    url(r'^(?P<id>.+)/$', 'interface_view', {}, name='interface_view'),
)