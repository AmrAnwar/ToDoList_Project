from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from ..models import List, Task, Sublist


class TestListView(TestCase):
    def setUp(self):
        self.client = Client()
        user = User(
            username='tester'
        )
        user.set_password('password')
        user.save()
        list = List(
            user=user,
            title="List TEST",
        ).save()
        task = Task(
            user=user,
            title="Task TEST",
            list=list,
        )
        sublist = Sublist(
            title="SubList TEST",
            task=task
        )


class TestList(TestListView):
    def test_list_view(self):
        self.client.force_login(User.objects.get(username='tester')[0])
        response = self.client.get("list-list")
        self.assertEqual(response.status_code, 200)
