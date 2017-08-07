# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated

from ..models import Task, Sublist, Comment
from ..serializers import (
    TaskFullModelSerializer,
    SubListModelSerializer,
    CommentModelSerializer,
)

from .helper import create_item


class TaskModelViewSet(viewsets.ModelViewSet):
    serializer_class = TaskFullModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Task.objects.active(user=user)
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
