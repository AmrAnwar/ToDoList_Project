import json
from django.core.urlresolvers import reverse
from .test_main import TestMain
from .helper import view_test, create_patch
from ..models import Task, List
from ..models.helper import upload_location

class TestListSecure(TestMain):
    def setUp(self):
        super(TestListSecure, self).setUp()
        self.client.login(username='tester', password='password')

    def test_list_view(self):
        data = {
            "title": "test",
        }
        view_test(test_obj="lists", self=self, url=self.list_url, data=data)

    def test_image(self):
        self.list.image = "accounts/1/amr.jpg"
        self.list.save()
        self.assertEqual(self.list.image, "accounts/1/amr.jpg")

    def test_create_task(self):
        create_patch(self=self, test_obj="tasks", url=self.create_task)
        # test today
        res = self.client.get("/tasks/?today=true")
        len_results = len(list(res.data.get('results')))
        self.assertEqual(len_results, Task.objects.count())
        # test all GET
        res = self.client.get("/tasks/?list=1&today=false&finished=true&q=test")
        self.assertEqual(res.status_code, 200)
        # test 400 error
        res = self.client.get("/tasks/?list=f")
        self.assertEqual(res.status_code, 400)
        # test create from list
        data = {
            'title': "tester",
            'user': 1,
            'list': 1,
        }
        res = self.client.post(self.task_url_list, json.dumps(data),
                               content_type='application/json')
        self.assertEqual(res.status_code, 201)

    def test_create_sublist(self):
        create_patch(self=self, test_obj="sublists", url=self.create_subtask)

    def test_add_user_post_request(self):
        add_url = reverse("lists-add-user", kwargs={'pk': self.list.id})
        remove_url = reverse("lists-remove-user", kwargs={'pk': self.list.id})
        data = {
            'user_id': self.guest.id
        }
        # add user not in list
        response = self.client.post(add_url, json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # add user in list
        response = self.client.post(add_url, json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)

        self.client.login(username='guest', password='password')
        # check if user was added
        response = self.client.get(self.list_url)
        length = len(response.data.get('results'))
        self.assertEqual(length, 1)
        # check search
        response = self.client.get("/lists/?search=noewwet")
        self.assertLess(len(response.data.get('results')), length)
        # check lists created by user
        response = self.client.get("/lists/?owner=true")
        self.assertEqual(len(response.data.get('results')), 0)

        self.client.login(username='tester', password='password')
        # remove user from list
        response = self.client.post(remove_url, json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # remove user not in list
        response = self.client.post(remove_url, json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        # check remove
        self.client.login(username='guest', password='password')
        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data.get('results')), 0)

    def test_upload_location(self):
        location = upload_location(self.list, "file")
        self.assertEqual(location, "list/1/file")
