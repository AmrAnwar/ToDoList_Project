from rest_framework import serializers


class EmailListSerializer(serializers.Serializer):
    """
    Serializer for make list of users id
    """
    email_list = serializers.ListField()

