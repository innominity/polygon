from rest_framework import serializers
from .models import RemoteApp, RemoteAppFileConfigType


class RemoteAppFileConfigTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = RemoteAppFileConfigType
        fields = ("id", "name", "is_required")
