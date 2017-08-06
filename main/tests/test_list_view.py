import json
from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils import timezone
from ..models import List, Task, Sublist
from helper import view_test, create_patch
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404

class TestListView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User(
            username='tester',
        )
        self.user.set_password('password')
        self.user.save()
        self.guest =User(
            username='guest',
        )
        self.guest.set_password("password")
        self.guest.save()

        self.list = List.objects.create(
            user=self.user,
            title="List TEST",
        )
        self.task = Task.objects.create(
            user=self.user,
            title="Task TEST",
            list=self.list,
        )
        self.sublist = Sublist.objects.create(
            title="SubList TEST",
            task=self.task
        )
        self.list_url = reverse("lists-list")
        self.task_url_list = reverse("tasks-list")
        self.create_task = reverse("lists-create",
                                   kwargs={'pk': 1})
        self.create_subtask = reverse("tasks-create",
                                      kwargs={'pk': 1})


class TestListSecure(TestListView):
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
        # res = self.client.get(reverse("sublists-list"))
        create_patch(self=self, test_obj="sublists", url=self.create_subtask)

    def test_add_list(self):
        add_url = reverse("add-list", kwargs={'list_id': self.list.id,
                                                   "user_id": self.guest.id})
        response = self.client.get(add_url)
        self.assertEqual(response.status_code, 200)
        add = response.data.get('add')
        self.assertEqual(add, True)

        self.client.login(username='guest', password='password')
        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data.get('results')), 1)

        self.client.login(username='tester', password='password')
        response = self.client.get(add_url)
        self.assertEqual(response.status_code, 200)
        add = response.data.get('add')
        self.assertEqual(add, False)

        self.client.login(username='guest', password='password')
        response = self.client.get(self.list_url)
        self.assertEqual(len(response.data.get('results')), 0)



    # def test_tasks(self):
    #     pass
    #     # data = {
    #     #     "title": "test",
    #     #     "list": model_to_dict(self.list),
    #     #     "user": model_to_dict(self.user),
    #     # }
    #     # response = self.client.post(self.task_url, data=json.simplejson.dumps(data),
    #     #                             content_type='application/json')
    #     # self.assertEqual(response.status_code, 201)
    #     # self.assertEqual(response.data.get('user'), self.user.id)
    #     # re_data = {
    #     #     "title": "re-test",
    #     # }
    #     # detail_url = "%s-detail" % "tasks"
    #     # new_list_url = reverse(detail_url,
    #     #                        kwargs={'pk': response.data.get('id')})
    #     # response = self.client.patch(new_list_url,
    #     #                              json.dumps(re_data),
    #     #                              content_type='application/json')
    #     # self.assertEqual(response.status_code, 200)
    #     # self.assertEqual(response.data.get('title'), 're-test')
    #     #
    #     # # view_test(test_obj="tasks", self=self, url=self.task_url, data=data)
