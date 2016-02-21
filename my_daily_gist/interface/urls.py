from django.conf.urls import patterns, include, url

urlpatterns =  patterns('interface.views',
    url(r'^$', 'interface_index', {}, name='interface_index'),
    url(r'^code/(?P<id>.+)/$', 'interface_view', {}, name='interface_view'),
    url(r'^sha1/$', 'sha1_view', {}, name='sha1_view'),
    url(r'^json_test/$', 'json_test', {}, name='json_test'),
    url(r'^\.well-known/acme-challenge/ilqDMoTOdWLoELgqOsd19jnre5PqySJ8ntYkEtkJ6DU/$', 'acme_challenge', {}, name='acme_challenge'),
    url(r'^image_converter/$', 'image_converter', {}, name='image_converter'),
)