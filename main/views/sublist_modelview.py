# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import viewsets
from ..models import Task, Sublist
from ..serializers import SubListModelSerializer
from rest_framework.decorators import detail_route


class SublistModelViewSet(viewsets.ModelViewSet):
    serializer_class = SubListModelSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Sublist.objects.active()
        return qs


