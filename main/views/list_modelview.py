# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets
from ..models import List, Task
from ..serializers import ListModelSerializer, TaskModelSerializer
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import get_user_lists
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from .helper import create_item


class ListModelViewSet(viewsets.ModelViewSet):

    serializer_class = ListModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # send_mail(
        #     'Subject here',
        #     'Here is the message.',
        #     'amranwar945@outlook.sa',
        #     ['amranwar945@gmail.com'],
        #     fail_silently=False,
        # )

        # subject, from_email, to = 'hello', 'amranwar945@gmail.com', 'amranwar945@gmail.com'
        # text_content = 'This is an important message.'
        # html_content = '<p>This is an <strong>important</strong> message.</p>'
        # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        # msg.attach_alternative(html_content, "text/html")
        # msg.send()
        qs = get_user_lists(user=self.request.user,)
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @detail_route(methods=['post'], url_path='create')
    def create_task(self, request, pk=None):
        return create_item('user',
                           'list',
                           request=request,
                           pk=pk,
                           Model=List,
                           ModelSerializer=Task,
                           Serializer=TaskModelSerializer,
                           self=self, )

