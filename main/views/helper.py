from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone


def create_item(*args, **kwargs):
    """
    Help Function to create objects
    :param args: if we want to handle string
    :param kwargs: if we want to send vars
    :return: 3 cases :
                1- if obj pk not found, return: 404
                2- if serializer not valid, return: serializer.errors
                3- if serializer valid and obj pk found, return created task data ,201
    """
    Serializer = kwargs['Serializer']
    pk = kwargs['pk']
    Model = kwargs['Model']
    ModelSerializer = kwargs['ModelSerializer']
    request = kwargs['request']
    obj = get_object_or_404(Model, pk=pk)
    serializer = Serializer(data=request.data)
    if serializer.is_valid():
        if 'user' in args:
            serializer.validated_data['user'] = request.user
        if 'task' in args:
            serializer.validated_data['task'] = obj
        if 'list' in args:
            serializer.validated_data['list'] = obj
        created_obj = ModelSerializer.objects.create(**serializer.validated_data)
        return Response(Serializer(created_obj).data, status=201)
    else:
        return Response(serializer.errors)


def filter_by_today(qs=None):
    new_qs = []
    for obj in qs:
        if obj.timestamp.now().date() == timezone.now().date():
            new_qs.append(obj.id)

    return qs.filter(id__in=new_qs)
