from json import dumps
from django.http import JsonResponse


class JSONResponse(object):
    @classmethod
    def Respond(cls, *, status: int, message: str, **kwargs):
        data = dict({
            'message': message
        })

        for (key, value) in kwargs.items():
            data[key] = value

        resp = JsonResponse({})
        resp.status_code = status
        resp.content = dumps(data)

        return resp
