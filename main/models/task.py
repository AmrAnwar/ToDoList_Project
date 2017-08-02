# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from .list import List
from django.conf import settings

# Create your models here.


class TaskManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(TaskManager, self).filter(archived=True)


class Task(models.Model):
    user = models.ForeignKey(User, default=1, related_name="task_users")
    title = models.CharField(null=False, blank=False, max_length=100)
    archived = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    list = models.ForeignKey(List, related_name="list_tasks")

    class Meta:
        ordering = ["-timestamp"]

    def __unicode__(self):
        return "sublist %s:%s"%(self.title, self.user)