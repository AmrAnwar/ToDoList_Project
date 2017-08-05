from rest_framework import serializers

from ..models import List, Task
from task_serializer import TaskModelSerializer
from .helper import get_data


class ListModelSerializer(serializers.ModelSerializer):
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = List
        fields = ('id', 'title', 'timestamp', 'archived', 'user', "tasks", "users")

    def get_tasks(self, obj):
        # return get_data(obj=obj, serializer=TaskModelSerializer, Child=Task)
        qs = Task.objects.filter(list=obj)
        qs_serializer = TaskModelSerializer(qs, many=True).data
        return qs_serializer
