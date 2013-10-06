from django.conf.urls import patterns, include, url

urlpatterns =  patterns('interface.views',
    url(r'^$', 'interface_index', {}, name='interface_index'),
)