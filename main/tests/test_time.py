import json

from django.utils import timezone
from .test_main import TestMain


class TestFinishTime(TestMain):
    def setUp(self):
        super(TestFinishTime, self).setUp()
        self.client.login(username='tester', password='password')

    def test_finished(self):
        data = {
            'finished': True,
        }
        self.client.patch(self.my_task_url, json.dumps(data), content_type='application/json')
        self.task.refresh_from_db()
        self.assertEqual(self.task.time_change, False)
        self.client.patch(self.my_task_url, json.dumps({'finished': False}), content_type='application/json')
        self.task.refresh_from_db()
        self.assertEqual(self.task.time_change, True)
