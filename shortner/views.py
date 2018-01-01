import re
import json
import uuid
from datetime import date


from django.views import View
from django.http import HttpRequest
from django.core.exceptions import ObjectDoesNotExist
from tinyurl.response import JSONResponse
from shortner.models import url


class CreateURL(View):
    """ This will parse and check for a valid url """
    def _parse_url(self, url_check: str):
        url_string = ''
        # just a quick and dirty check for http://
        if not re.search(r'^(https?:\/\/)', url_check, re.IGNORECASE):
            url_string += 'http://'

            if not re.search(r'^(www.)', url_check, re.IGNORECASE):
                url_string += 'www.'

        return "{}{}".format(url_string, url_check.lower())


    """ Creates a small url from the original url sent
        required JSON object {
            url: the original url
            expiration: the optional expiration date {
                year: number,
                month: number,
                day: number
            }
        }
        returned JSON object {
            url: the shortened url
            original: the original url,
            count: the url usage count
            expiration: the expiration date
        }
    """
    def post(self, request: HttpRequest):
        try:
            json_req = json.loads(request.body.decode('UTF-8'))
        except json.JSONDecodeError:
            return JSONResponse.Respond(status=403, message='received bad POST request data')

        if json_req.get('url', False) is False:
            return JSONResponse.Respond(status=403, message='no url found in request')

        url_id = uuid.uuid4().time_mid
        while url.objects.filter(url_hash__exact=url_id).exists():
            url_id = uuid.uuid4().time_mid

        today = date.today()
        new_url = url()

        if json_req.get('expiration', False) is False:
            expiration = date(year=today.year + 1, month=today.month, day=today.day)
        else:
            try:
                expiration = date(
                    year=json_req['expiration']['year'],
                    month=json_req['expiration']['month'],
                    day=json_req['expiration']['day']
                )
            except ValueError:
                expiration = date(year=today.year + 1, month=today.month, day=today.day)

        new_url.long_name = self._parse_url(json_req.get('url', ''))
        new_url.url_hash = url_id
        new_url.usage_count = 0
        new_url.expiration_date = expiration
        new_url.save()

        return JSONResponse.Respond(
            status=200,
            message='success',
            url=new_url.url_hash,
            count=0,
            original=new_url.long_name,
            expiration=new_url.expiration_date.isoformat()
        )


class Expiration(View):
    """ GET: Return the expiration date for a given shortened url
        return JSON object {
            url: the url hash,
            expiration: the expiration date
        }
        POST: Set the expiration date to a given shortened url
        required JSON object {
            url: the url hash,
            expiration: {
                year: number,
                month: number,
                day: number
            }
        }
    """

    def get(self, request: HttpRequest, url_hash: str):
        try:
            query_url = url.objects.get(url_hash__exact=url_hash)
        except ObjectDoesNotExist:
            return JSONResponse.Respond(status=403, message='Could not find url hash {}'.format(url_hash))

        return JSONResponse.Respond(
            status=200,
            message='success',
            url=url_hash,
            expiration=query_url.expiration_date.isoformat()
        )

    def post(self, request: HttpRequest):
        try:
            req_json = json.loads(request.body.decode('UTF-8'))
        except json.JSONDecodeError:
            return JSONResponse.Respond(status=403, message='incorrect data sent to the server')

        try:
            query_url = url.objects.get(url_hash__exact=req_json.get('url'))
        except ObjectDoesNotExist:
            return JSONResponse.Respond(status=403, message='Could not find url hash {}'.format(req_json.get('url')))

        exp_obj = req_json.get('expiration')
        exp_date = date(year=exp_obj.get('year'), month=exp_obj.get('month'), day=exp_obj.get('day'))

        query_url.expiration_date = exp_date
        query_url.save(update_fields=['expiration_date'])

        return JSONResponse.Respond(
            status=200,
            message='success',
            url=query_url.url_hash,
            expiration=exp_date.isoformat()
        )


class Usage(View):
    """ return or set the click (usage) count of the url
        GET: returned JSON object {
            url: the short url,
            count: the click count
        }
        POST: required JSON object {
            url: the url hash,
            count: the click count
        }
    """

    def get(self, request: HttpRequest, url_hash: str):
        try:
            query_url = url.objects.get(url_hash__exact=url_hash)
        except ObjectDoesNotExist:
            return JSONResponse.Respond(status=403, message='Could not find url hash {}'.format(url_hash))

        return JSONResponse.Respond(status=200, message='success', url=query_url.url_hash, count=query_url.usage_count)

    def post(self, request: HttpRequest):
        try:
            req_json = json.loads(request.body.decode('UTF-8'))
        except json.JSONDecodeError:
            return JSONResponse.Respond(status=403, message='received bad POST request data')

        try:
            query_url = url.objects.get(url_hash__exact=req_json.get('url'))
        except ObjectDoesNotExist:
            return JSONResponse.Respond(status=403, message='Could not find url hash {}'.format(req_json.get('url')))

        query_url.usage_count += 1
        query_url.save()
        return JSONResponse.Respond(status=200, message='success', count=query_url.usage_count)


class OriginalUrl(View):
    """ returns the original url the hash is pointing to
        returned JSON object {
            'url': the shorten url,
            'original': the original url
        }
    """

    def get(self, request: HttpRequest, url_hash: str):
        try:
            query_url = url.objects.get(url_hash__exact=url_hash)
        except ObjectDoesNotExist:
            return JSONResponse.Respond(status=403, message='Could not find url hash {}'.format(url_hash))

        return JSONResponse.Respond(
            status=200,
            message='success',
            url=query_url.url_hash,
            original=query_url.long_name,
            count=query_url.usage_count,
            expiration=query_url.expiration_date.isoformat()
        )
