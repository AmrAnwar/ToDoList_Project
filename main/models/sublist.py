# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from .task import Task
# Create your models here.


class SubListManager(models.Manager):
    """
    Sublist Manger
    """
    def active(self, *args, **kwargs):
        return super(SubListManager, self).filter(archived=False)


class Sublist(models.Model):
    """
    Sublist Model appears in Task Detail and Serializer
    """
    title = models.CharField(null=False, blank=False, max_length=100)
    archived = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, related_name="task_sublist")

    objects = SubListManager()

    class Meta:
        ordering = ["-timestamp"]

    def __unicode__(self):
        return "sublist %s" % self.title
