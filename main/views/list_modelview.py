# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import viewsets
from ..models import List, Task
from ..serializers import ListModelSerializer, TaskModelSerializer
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.core.urlresolvers import reverse


class ListModelViewSet(viewsets.ModelViewSet):
    serializer_class = ListModelSerializer

    def get_queryset(self):
        user = self.request.user
        qs = List.objects.active(user=user)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @detail_route(methods=['post'], url_path='create')
    def create_task(self, request, pk=None):
        serializer = TaskModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.validated_data['list'] = List.objects.get(pk=pk)
            task = Task.objects.create(**serializer.validated_data)

            return Response(TaskModelSerializer(task).data, status=201)

        else:
            return serializer.errors
