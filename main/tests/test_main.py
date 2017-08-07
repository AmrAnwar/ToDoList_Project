from PIL import Image
import tempfile
from django.test import Client, TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from ..models import List, Task, Sublist

image = Image.new('RGB', (100, 100))
tmp_file = tempfile.NamedTemporaryFile(suffix='.bmp')
image.save(tmp_file)


class TestMain(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User(
            username='tester',
            email='amranwar945@gmail.com',
        )
        self.user.set_password('password')
        self.user.save()
        self.guest = User(
            username='guest',
            email='amranwar714@gmail.com',

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
        self.my_task_url = reverse("tasks-detail",
                                   kwargs={'pk': self.task.pk})
        self.create_subtask = reverse("tasks-sublist",
                                      kwargs={'pk': 1})
