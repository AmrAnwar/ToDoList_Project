from rest_framework import serializers


class AddUserListSerializer(serializers.Serializer):
    """
    serializer for user to a list
    """
    user_id = serializers.CharField(required=True)
