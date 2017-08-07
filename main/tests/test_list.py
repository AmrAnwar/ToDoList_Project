import json
from .test_main import TestMain
from .helper import view_test, create_patch
from django.core.urlresolvers import reverse


class TestListSecure(TestMain):
    def setUp(self):
        super(TestListSecure, self).setUp()
        self.client.login(username='tester', password='password')

    def test_list_view(self):
        data = {
            "title": "test",
        }
        view_test(test_obj="lists", self=self, url=self.list_url, data=data)

    def test_create_task(self):
        create_patch(self=self, test_obj="tasks", url=self.create_task)

    def test_create_sublist(self):
        create_patch(self=self, test_obj="sublists", url=self.create_subtask)

    def test_add_user_post_request(self):
        add_url = reverse("lists-add-user", kwargs={'pk': self.list.id})
        remove_url = reverse("lists-remove-user", kwargs={'pk': self.list.id})
        data = {
            'user_id': self.guest.id
        }
        # add user not in list
        response = self.client.post(add_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # add user in list
        response = self.client.post(add_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        self.client.login(username='guest', password='password')
        # check if user was added
        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data.get('results')), 1)

        self.client.login(username='tester', password='password')
        # remove user from list
        response = self.client.post(remove_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.client.login(username='guest', password='password')
        # remove user not in list

        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data.get('results')), 0)


