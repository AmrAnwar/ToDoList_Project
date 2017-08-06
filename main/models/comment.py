from __future__ import unicode_literals
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from .task import Task


class Comment(models.Model):
    user = models.ForeignKey(User, default=1)
    content = models.TextField()
    parent = models.ForeignKey("self", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="comments_like")
    task = models.ForeignKey(Task, related_name="comments_task")

    class Meta:
        ordering = ['-timestamp']

    def __unicode__(self):
        return str(self.content[:10])

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

