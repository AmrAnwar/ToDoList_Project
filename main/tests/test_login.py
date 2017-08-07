from django.core.urlresolvers import reverse
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

