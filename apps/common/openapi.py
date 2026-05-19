from drf_spectacular.utils import inline_serializer
from rest_framework import serializers


def envelope(name, data_field=None):
    """Inline serializer that mirrors the APIResponse envelope for OpenAPI schemas."""
    return inline_serializer(
        name=name,
        fields={
            "status_code": serializers.IntegerField(),
            "message": serializers.CharField(),
            "data": data_field or serializers.JSONField(allow_null=True),
            "errors": serializers.JSONField(allow_null=True),
        },
    )
