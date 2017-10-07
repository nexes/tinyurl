from datetime import date
from tinyurl.response import JSONResponse
from shortner.models import url

from django.views import View
from django.http import HttpRequest, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist


class RouteToIndex(View):
    """ This will serve the static files """

    def get(self, request: HttpRequest):
        return JSONResponse.Respond(status=200, message='what index')


class RouteToUrl(View):
    """ This will redirct to the actual url stored """

    def get(self, request: HttpRequest, url_hash: str):
        try:
            query_url = url.objects.get(url_hash__exact=url_hash)
        except ObjectDoesNotExist:
            return JSONResponse.Respond(status=301, message='url hash {} was not found'.format(url_hash))

        today = date.today()
        expire = query_url.expiration_date

        if (expire - today).days > 0:
            query_url.usage_count += 1
            query_url.save()
            return HttpResponseRedirect(query_url.long_name)
        else:
            return JSONResponse.Respond(status=400, message='url hash {} has expired'.format(url_hash))
