"""
Serializers for the user API view.
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers

MIN_PASSWORD_LEN = 8


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        """
        `model`, `fields` & `extra_kwargs` are meaningful variable names.
        e.g. changing `extra_kwargs` to `extra_params` basically renders it useless.
        extra_kwargs: password$write_only being True, removes password from response
        """
        model = get_user_model()  # the model the serializer represents.
        fields = ['email', 'password', 'name']   # fields provided in the request.
        # write_only: True; user can only set the password; api won't return it.
        extra_kwargs = {'password': {
            'write_only': True,
            'min_length': MIN_PASSWORD_LEN
        }}

    def create(self, validated_data):
        """Create & return a user with encrypted password."""
        # Additional layer so that we serialize only the validated data;
        # and not simply what the user provides. This way, the encrypted password
        # will be used, and not the raw password provided by user.
        return get_user_model().objects.create_user(**validated_data)
