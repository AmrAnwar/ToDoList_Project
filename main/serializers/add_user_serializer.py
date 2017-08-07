from rest_framework import serializers


class AddUserListSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True)
    # list_id = serializers.CharField(required=True)
