# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from .list import List


# from .sublist import Sublist

# Create your models here.

class TaskManager(models.Manager):
    def active(self, *args, **kwargs):
        try:
            if kwargs['user']:
                user = kwargs['user']
                return super(TaskManager, self).filter(archived=False, user=user)
        except:
            return super(TaskManager, self).filter(archived=False)


class Task(models.Model):
    user = models.ForeignKey(User, default=1, related_name="task_users")
    title = models.CharField(null=False, blank=False, max_length=100)
    archived = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    list = models.ForeignKey(List, related_name="list_tasks")
    objects = TaskManager()

    class Meta:
        ordering = ["-timestamp"]

    def __unicode__(self):
        return "task %s:%s:%s" % (self.title, self.list.title, self.user)

        # @property
        # def tasks(self):
        #     return Sublist.objects.filter(task=self)
        #
        # @property
        # def tasks(self):
        #     return Task.objects.filter(list=self.list)


def get_list_tasks(list):
    return Task.objects.filter(list=list)
