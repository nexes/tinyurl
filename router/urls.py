from django.conf.urls import url
from router.views import RouteToUrl, RouteToIndex


app_name = 'router'

urlpatterns = [
    url(r'^$', RouteToIndex.as_view(), name="index"),
    url(r'^(?P<url_hash>[0-9]+)/$', RouteToUrl.as_view(), name="route-hash")
]
