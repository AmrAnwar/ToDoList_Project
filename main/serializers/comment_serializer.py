from rest_framework import serializers
from ..models import Comment


class CommentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'content', 'timestamp', 'parent', 'user')


