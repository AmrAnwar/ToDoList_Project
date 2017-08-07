from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.serializers import (
    CharField,
    EmailField,
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)


class LoginSerializer(serializers.ModelSerializer):
    username = CharField(required=False, allow_blank=True)
    email = EmailField(label='Email Address', required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {"password":
            {
                "write_only": True,
            }
        }

    def validate(self, data):
        email = data.get("email", None)
        username = data.get("username", None)
        password = data.get("password", None)
        if not email and not username:
            raise ValidationError("A username or email is required to login")
        user = User.objects.filter(
            Q(email=email) |
            Q(username=username)
        ).distinct()
        user = user.exclude(email__isnull=True).exclude(email__iexact='')
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username/email is not valid")
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials please try again")
        data['username'] = user_obj.username
        data['email'] = user_obj.email
        return data
