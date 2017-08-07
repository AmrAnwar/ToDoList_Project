# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from .list import List
# from .sublist import Sublist

# Create your models here.

class TaskManager(models.Manager):
    def active(self, *args, **kwargs):
        """
        filter archived objs or archived and specific user Lists
        :param args:
        :param kwargs:
        :return: Queryset of lists filtered by archived element or archived and user
        """
        if kwargs['user']:
                user = kwargs['user']
                return super(TaskManager, self).filter(archived=False, user=user)


class Task(models.Model):
    """
    Task Model appears in List Detail and Has ModelViewSet
    """
    user = models.ForeignKey(User, default=1, related_name="task_users")
    title = models.CharField(null=False, blank=False, max_length=100)
    archived = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    finished = models.BooleanField(default=False)
    time_change = models.BooleanField(default=True)
    finished_time = models.DateTimeField(auto_now_add=False,
                                         null=True, blank=True, default=None)
    list = models.ForeignKey(List, related_name="list_tasks")
    objects = TaskManager()

    class Meta:
        ordering = ["-timestamp"]

    def __unicode__(self):
        return "task %s" % self.title

    def save(self, *args, **kwargs):
        """
        check finished to change finished_time
        :param args:
        :param kwargs:
        :return:
        """
        if self.finished and self.time_change:
            self.finished_time = timezone.now()
            self.time_change = False
        if not self.finished and not self.time_change:
            self.time_change = True
        super(Task, self).save()


def list_tasks(list_id):
    return Task.objects.filter(list=list_id)
