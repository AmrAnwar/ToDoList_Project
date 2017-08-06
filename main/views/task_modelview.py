# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework import viewsets
from ..models import Task, Sublist
from ..serializers import TaskFullModelSerializer, SubListModelSerializer
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from ..permissions import IsInTask
from rest_framework.permissions import IsAuthenticated


class TaskModelViewSet(viewsets.ModelViewSet):
    serializer_class = TaskFullModelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Task.objects.active(user=user)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @detail_route(methods=['post'], url_path='create')
    def create_sublist(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
        except:
            return Response(status=404)
        serializer = SubListModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['task'] = task
            sublist = Sublist.objects.create(**serializer.validated_data)
            return Response(SubListModelSerializer(sublist).data, status=201)
        else:
            return Response(serializer.errors)

    @detail_route(methods=['post'], url_path='create-comment')
    def create_comment(self, request, pk=None):
        try:
            task = Task.objects.get(pk=pk)
        except:
            return Response(status=404)
        serializer = CommentSerilizer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['task'] = task
            sublist = Sublist.objects.create(**serializer.validated_data)
            return Response(SubListModelSerializer(sublist).data, status=201)
        else:
            return Response(serializer.errors)