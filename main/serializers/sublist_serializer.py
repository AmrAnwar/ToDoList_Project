from rest_framework import serializers

from ..models import Sublist


class SubListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sublist
        fields = ('id', 'title', 'timestamp', 'archived',)

