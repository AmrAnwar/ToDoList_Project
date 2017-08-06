from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from ..models import List
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class AddToList(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request, list_id=None, user_id=None, format=None):
        list = get_object_or_404(List, id=list_id)
        user = self.request.user
        add = False
        updated = False
        if user == list.user:
            if user.is_authenticated():
                new_user = get_object_or_404(User, id=user_id)
                if new_user in list.users.all():
                    add = False
                    list.users.remove(new_user)
                else:
                    add = True
                    list.users.add(new_user)
                updated = True
        else:
            return Response(status=404)
        data = {
            'add': add,
            'updated': updated,
        }
        return Response(data)
