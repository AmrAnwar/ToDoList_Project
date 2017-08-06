# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import viewsets
from ..models import List, Task
from ..serializers import ListModelSerializer, TaskModelSerializer
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.core.urlresolvers import reverse
from ..permissions import IsInList
from rest_framework.permissions import IsAuthenticated
from ..models import get_user_lists


class ListModelViewSet(viewsets.ModelViewSet):
    serializer_class = ListModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = get_user_lists(user=self.request.user,)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def perform_update(self, serializer):

    @detail_route(methods=['post'], url_path='create')
    def create_task(self, request, pk=None):
        serializer = TaskModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.validated_data['list'] = List.objects.get(pk=pk)
            task = Task.objects.create(**serializer.validated_data)

            return Response(TaskModelSerializer(task).data, status=201)
        else:
            return Response(serializer.errors)
