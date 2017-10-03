import json
from django.test import TestCase, Client
# from shortner.models import url


class CreateUrlTestCase(TestCase):
    def setUp(self):
        self.url = '/api/shortner/create/'

    def test_url_creation(self):
        client = Client()
        no_exp = client.post(self.url, json.dumps({
            'url': 'www.google.com'
        }), content_type='application/json')

        with_exp = client.post(self.url, json.dumps({
            'url': 'www.google.com',
            'expiration': {
                'year': 2010,
                'month': 2,
                'day': 13
            }
        }), content_type='application/json')

        self.assertEqual(no_exp.status_code, 200)
        print('\tCreation with default expiration: 200')
        print('\texpiration: {}'.format(no_exp.json()['expiration']))
        print('\tshort url: {}\n'.format(no_exp.json()['url']))

        self.assertEqual(with_exp.status_code, 200)
        print('\tCreation with custom expiration: 200')
        print('\texpiration: {}'.format(with_exp.json()['expiration']))
        print('\tshort url: {}\n'.format(with_exp.json()['url']))


class ExpireUrlTestCase(TestCase):
    def setUp(self):
        no_exp = Client().post('/api/shortner/create/', json.dumps({
            'url': 'www.google.com'
        }), content_type='application/json')

        _url = no_exp.json()['url']
        self.url_hash = _url[_url.rfind('/') + 1:]
        self.url = '/api/shortner/expiration/'

    def test_url_expire(self):
        client = Client()
        exp_resp = client.post(self.url, json.dumps({
            'url': self.url_hash,
            'expiration': {
                'year': 2020,
                'month': 12,
                'day': 25
            }
        }), content_type='application/json')

        self.assertEqual(exp_resp.status_code, 200)
        print('\tExpiration date was set: 200')
        print('\texpiration date {}\n'.format(exp_resp.json()['expiration']))

        get_resp = client.get('{}{}/'.format(self.url, self.url_hash), content_type='application/json')

        self.assertEqual(get_resp.status_code, 200)
        print('\tReturned correct expiration date: {}\n'.format(get_resp.json()['expiration']))
