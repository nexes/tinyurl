from django.conf.urls import url
from shortner.views import (
    CreateURL,
    Expiration,
    Usage,
    OriginalUrl
)


app_name = 'shortner'

urlpatterns = [
    url(r'^create/$', CreateURL.as_view(), name='create'),
    url(r'^expiration/$', Expiration.as_view(), name='set-expiration'),
    url(r'^expiration/(?P<url_hash>[a-zA-Z0-9]+)/$', Expiration.as_view(), name='get-expiration'),
    url(r'^usage/$', Usage.as_view(), name='set-usage'),
    url(r'^usage/(?P<url_hash>[a-zA-Z0-9]+)/$', Usage.as_view(), name='get-usage'),
    url(r'^original/(?P<url_hash>[a-zA-Z0-9]+)/$', OriginalUrl.as_view(), name='get-original')
]
