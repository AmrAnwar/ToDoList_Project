from rest_framework import serializers

from ..models import Task, Sublist
from .sublist_serializer import SubListModelSerializer


class TaskFullModelSerializer(serializers.ModelSerializer):
    sublist = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'user', 'title', 'timestamp', 'archived', 'sublist')

    def get_sublist(self, obj):
        qs = Sublist.objects.filter(task=obj)
        qs_serializer = SubListModelSerializer(qs, many=True).data
        return qs_serializer
