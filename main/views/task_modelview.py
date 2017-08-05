# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import viewsets
from ..models import Task
from ..serializers import TaskModelSerializer
from rest_framework.decorators import detail_route


class TaskModelViewSet(viewsets.ModelViewSet):
    serializer_class = TaskModelSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Task.objects.active(user=user)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @detail_route(methods=['post'], url_path='create')
    def create_task(self, request, pk=None):
        serializer = TaskModelSerializer(data=request.data)
        if serializer.is_valid():
            print "LOOOL"
            serializer.validated_data['user'] = request.user.id
        else:
            print "LOL"