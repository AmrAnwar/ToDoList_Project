# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
# Create your models here.


class ListManager(models.Manager):
    def active(self, *args, **kwargs):
        try:
            if kwargs['user']:
                user = kwargs['user']
                return super(ListManager, self).filter(archived=False, user=user)
        except:
            return super(ListManager, self).filter(archived=False)


class List(models.Model):
    user = models.ForeignKey(User, default=1, related_name="users")
    title = models.CharField(null=False, blank=False, max_length=100)
    archived = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ListManager()

    class Meta:
        ordering = ["-timestamp"]

    def __unicode__(self):
        return "list %s:%s" % (self.title, self.user)
