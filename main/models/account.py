from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, default=1)
    image = models.CharField(max_length=20, default="null")
    token = models.CharField(max_length=500)


def create_profile(sender, instance, **kwargs):
    if kwargs['created']:
            UserProfile(user=instance).save()

post_save.connect(create_profile, sender=User)
