# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from ..models import Sublist
from ..serializers import SubListModelSerializer


class SublistModelViewSet(viewsets.ModelViewSet):
    """
    Model ViewSet For SubLists
    """
    serializer_class = SubListModelSerializer

    def get_queryset(self):
        return Sublist.objects.active()


