from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save


def upload_location(instance, filename):
    return "accounts/%s/%s" % (instance.id, filename)


class UserProfile(models.Model):
    user = models.OneToOneField(User, default=1)
    token = models.CharField(max_length=500, null=True, blank=True)
    image = models.ImageField(
        upload_to=upload_location,
        null=True, blank=True,
        height_field='height_field',
        width_field='width_field',
    )
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)

    def __str__(self):
        return "%s" % self.user.username


def create_profile(sender, instance, **kwargs):
    if kwargs['created']:
        UserProfile(user=instance).save()


post_save.connect(create_profile, sender=User)
