from rest_framework import serializers
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    """Serializer for login"""

    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        if not username or not password:
            raise serializers.ValidationError("Username and password are required")

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("User is not active")

        attrs["user"] = user
        return attrs


