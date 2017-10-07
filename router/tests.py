import json
from django.test import TestCase, Client


class RouteTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        resp = self.client.post('/api/shortner/create/', json.dumps({
            'url': 'https://docs.djangoproject.com/en/1.11/topics/http/shortcuts'
        }), content_type='application/json')

        _url = resp.json()['url']
        self.url_hash = _url[_url.rfind('/') + 1:]
        self.url = '/'

    def test_redirect(self):
        resp = self.client.get('{}{}/'.format(self.url, self.url_hash), follow=True)

        print(resp.redirect_chain)
        self.assertRedirects(resp, 'https://docs.djangoproject.com/en/1.11/topics/http/shortcuts')
