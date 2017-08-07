from rest_framework import serializers

from ..models import Task


class TaskModelSerializer(serializers.ModelSerializer):
    """
    Task Model Serializer
    """
    class Meta:
        model = Task
        fields = ('id', 'user', 'title', 'timestamp', 'archived',
                  'finished', 'finished_time',)

