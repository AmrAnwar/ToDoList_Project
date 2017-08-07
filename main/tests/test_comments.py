import json
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from .test_main import TestMain
from ..models import Comment


class TestComments(TestMain):
    def setUp(self):
        super(TestComments, self).setUp()
        self.client.login(username='tester', password='password')

    def test_create_comment(self):
        create_comment_url = reverse("tasks-comment",
                                     kwargs={'pk': 1})
        data = {
            'content': "comment"
        }
        count = Comment.objects.count()
        res = self.client.post(create_comment_url,
                               data=json.dumps(data),
                               content_type='application/json')
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Comment.objects.count(), count+1)
        # get object
        comment = get_object_or_404(Comment, pk=1)
        # test children method
        self.assertEqual(list(comment.children()), [])
        self.assertEqual(unicode(comment), "comment")
        res = self.client.get(reverse("tasks-detail",
                                      kwargs={'pk': 1}))
        comments = res.data.get('comments')
        self.assertEqual(len(comments), 1)
