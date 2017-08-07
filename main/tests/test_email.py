import json
from django.core import mail
from django.core.urlresolvers import reverse
from .test_main import TestMain


class TestEmailSend(TestMain):
    def setUp(self):
        super(TestEmailSend, self).setUp()
        self.client.login(username='tester', password='password')

    def test_send_email(self):
        send_url = reverse("lists-send-email",
                           kwargs={'pk': self.list.id})
        data = {
            'email_list': [1, 2]
        }
        res = self.client.post(send_url, json.dumps(data), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)