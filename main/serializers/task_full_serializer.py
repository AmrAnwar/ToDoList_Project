from rest_framework import serializers

from ..models import Task, Sublist, Comment
from .sublist_serializer import SubListModelSerializer
from .comment_serializer import CommentModelSerializer


class TaskFullModelSerializer(serializers.ModelSerializer):
    """
    Serializer for Tasks
    But has 2 more MethodFields for SubLists, Comments
    """
    sublist = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ('id', 'user', 'title', 'timestamp', 'archived', 'sublist', 'comments',
                  'finished', 'finished_time', 'list')

    def get_sublist(self, obj):
        """
        filter SubList by Task obj
        :param obj: Task obj
        :return: queryset of SubLists for specific Task obj
        """
        qs = Sublist.objects.filter(task=obj)
        qs_serializer = SubListModelSerializer(qs, many=True).data
        return qs_serializer

    def get_comments(self, obj):
        """
        filter Comments by Task obj
        :param obj: Task obj
        :return: queryset of Comments for specific Task obj
        """
        qs = Comment.objects.filter(task=obj)
        qs_serializer = CommentModelSerializer(qs, many=True).data
        return qs_serializer
