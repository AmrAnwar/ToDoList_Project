from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .test_main import TestMain
import json


class TestLogIn(TestMain):
    def setUp(self):
        super(TestLogIn, self).setUp()

    def test_view_without_login(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 403)

    def test_login(self):
        url = reverse("login")
        data = {
            'username': "tester",
            'password': "password",
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        count = User.objects.count()
        data_valid = {'username': "erg", "password": "rgrdg"}  # valid but not real user
        data_wrong_pass = {'username': 'tester', "password": 'my_password'}  # wrong pass
        data_un_valid = {'my_username': 'test'}
        data_empty = {'username': None, 'password': None, 'email': None}
        self.client.post(url, json.dumps(data_valid), content_type='application/json')
        self.client.post(url, json.dumps(data_wrong_pass), content_type='application/json')
        self.client.post(url, json.dumps(data_un_valid), content_type='application/json')
        self.client.post(url, json.dumps(data_empty), content_type='application/json')

        self.assertEqual(count, User.objects.count())

