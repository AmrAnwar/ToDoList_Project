# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from ..models import Task, Sublist, Comment, list_tasks
from ..serializers import (
    TaskFullModelSerializer,
    SubListModelSerializer,
    CommentModelSerializer,
)

from .helper import create_item, filter_by_today


class TaskModelViewSet(viewsets.ModelViewSet):
    serializer_class = TaskFullModelSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ('title', 'list')
    # filter_fields = ('list',)

    def get_queryset(self):
        list = self.request.GET.get("list")
        search = self.request.GET.get("q")
        finished = self.request.GET.get("finished")
        today = self.request.GET.get("today")
        qs = Task.objects.active(user=self.request.user)
        if list:
            try:
                qs = list_tasks(int(list))
            except:
                raise ValidationError("enter integer")
        if finished == 'true':
            qs = qs.filter(finished=True)
        if search:
            qs = qs.filter(title__icontains=search)
        if today == 'false':
            qs = qs.filter(timestamp__lt=timezone.now())
        if today == 'true':
            qs = filter_by_today(qs)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @detail_route(methods=['post'], url_path='sublist')
    def create_sublist(self, request, pk=None):
        return create_item(
            'task',
            request=request,
            pk=pk,
            Model=Task,
            ModelSerializer=Sublist,
            Serializer=SubListModelSerializer,
            self=self, )

    @detail_route(methods=['post'], url_path='comment')
    def create_comment(self, request, pk=None):
        return create_item('user',
                           'task',
                           request=request,
                           pk=pk,
                           Model=Task,
                           ModelSerializer=Comment,
                           Serializer=CommentModelSerializer,
                           self=self, )
