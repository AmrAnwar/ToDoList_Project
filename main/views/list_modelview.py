# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core import mail

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from rest_framework.response import Response

from ..models import get_user_lists, List, Task
from ..serializers import (
    ListModelSerializer,
    TaskModelSerializer,
    AddUserListSerializer,
    EmailListSerializer
)
from .helper import create_item


class ListModelViewSet(viewsets.ModelViewSet):
    """
    List Model View Set
    """
    serializer_class = ListModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        get lists method
        :return: 2 cases
            1- /lists , queryset(lists) if user in it
            2- /?owner=true , the lists which were created by user
        """
        owner = self.request.GET.get("owner")
        query = self.request.GET.get("search")
        qs = get_user_lists(user=self.request.user, )
        if query:
            qs = qs.filter(title__icontains=query)
        if owner == 'True' or owner == 'true':
            qs = List.objects.active(user=self.request.user)

        return qs

    def perform_create(self, serializer):
        """
        save user in a list serializer
        :param serializer:
        """
        serializer.save(user=self.request.user)

    @detail_route(methods=['post'], url_path='create')
    def create_task(self, request, pk=None):
        """
        Create New Task
        :param pk: user list pk
        :return:
            3 cases :
                1- if obj pk not found, return: 404
                2- if serializer not valid, return: serializer.errors
                3- if serializer valid and obj pk found, return created task data
        """
        return create_item('user',
                           'list',
                           request=request,
                           pk=pk,
                           Model=List,
                           ModelSerializer=Task,
                           Serializer=TaskModelSerializer,
                           self=self, )

    @detail_route(methods=['post'], url_path='add-user')
    def add_user(self, request, pk=None):
        """
        Add new User to a List
        :param request:
        :param pk: list primary key
        :return: 4 cases :
                1- if not list or user , return: 404
                2- if user in list , return: ValidationError
                2- if serializer not valid, return: serializer.errors
                3- if serializer valid and obj pk found, not in list, return 200
        """
        serializer = AddUserListSerializer(data=request.data)
        # valid in all cases
        if serializer.is_valid(raise_exception=True):
            user_id = serializer.data.get("user_id")
            list = get_object_or_404(List, pk=pk)
            user = get_object_or_404(User, id=user_id)
            if user not in list.users.all():
                list.users.add(user)
                return Response(status=200)
            else:
                raise ValidationError("user is already in the list")

    @detail_route(methods=['post'], url_path='remove-user', )
    def remove_user(self, request, pk=None):
        """
        Remove User From List
        :param pk: list primary key
        :return: 4 cases :
                1- if not list or user , return: 404
                2- if user not in list , return: ValidationError
                2- if serializer not valid, return: serializer.errors
                3- if serializer valid and obj pk found, not in list, return 200
        """
        serializer = AddUserListSerializer(data=request.data)
        # valid in all cases
        if serializer.is_valid(raise_exception=True):
            user_id = serializer.data.get("user_id")
            list = get_object_or_404(List, pk=pk)
            user = get_object_or_404(User, id=user_id)
            if user in list.users.all():
                list.users.remove(user)
                return Response(status=200)
            else:
                raise ValidationError("user isn't in the list")

    @detail_route(methods=['post'], url_path='send-email', )
    def post(self, request, pk=None):
        """
        :param pk: list primary key
        :return: 2 cases :
            1- if serializer is'nt valid return serializer.errors
            2- if serializer is valid and obj pk exists, return 200 and send mails
        """
        list = get_object_or_404(List, pk=pk)
        serializer = EmailListSerializer(data=request.data)
        # valid in all cases
        if serializer.is_valid(raise_exception=True):
            id_list = serializer.data.get('email_list')
            email_list = [get_object_or_404(User, pk=pk).email for pk in id_list]
            mail.send_mail("check my list: %s" % list.title,
                           "url : %s" % list.get_url(),
                           "amranwar945@gamil.com",
                           email_list)
            return Response(status=200)
