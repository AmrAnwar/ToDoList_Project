# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from .helper import upload_location


class ListManager(models.Manager):
    def active(self, **kwargs):
        """
        filter archived objs or archived and specific user Lists
        :param args:
        :param kwargs:
        :return: Queryset of lists filtered by archived element or archived and user
        """
        try:
            if kwargs['user']:
                user = kwargs['user']
                return super(ListManager, self).filter(archived=False, user=user)
        except:
            return super(ListManager, self).filter(archived=False)


class List(models.Model):
    """
    the List Model
    """
    user = models.ForeignKey(User, default=1, related_name="users")
    title = models.CharField(null=False, blank=False, max_length=100)
    archived = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True,
                                   related_name="list_users")

    image = models.ImageField(
        upload_to=upload_location,
        null=True, blank=True,
        height_field='height_field',
        width_field='width_field',
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    objects = ListManager()

    class Meta:
        ordering = ["-timestamp"]

    def __unicode__(self):
        return "list %s" % self.title

    def get_url(self):
        """
        get detail url for List object
        :return: list detail url
        """
        return reverse("lists-detail", kwargs={'pk': self.id})


def get_user_lists(user=None):
    """
    get all user lists
    :param user:
    :return:
    """
    list_qs = [list.id for list in List.objects.active()
               if user in list.users.all() or user == list.user]
    return List.objects.filter(id__in=list_qs)

