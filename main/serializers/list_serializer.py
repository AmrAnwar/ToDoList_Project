from rest_framework import serializers

from ..models import List, Task
from task_serializer import TaskModelSerializer


class ListModelSerializer(serializers.ModelSerializer):
    """
    List Model Serializer
    """
    tasks = serializers.SerializerMethodField()

    class Meta:
        model = List
        fields = ('id', 'title', 'timestamp', 'image',
                  'archived', 'user', "tasks", "users",)

    def get_tasks(self, obj):
        """
        filter Tasks by my List obj
        :param obj: List obj
        :return: tasks to specific List obj
        """
        qs = Task.objects.filter(list=obj)
        qs_serializer = TaskModelSerializer(qs, many=True).data
        return qs_serializer
