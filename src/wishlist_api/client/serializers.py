from rest_framework import serializers

from wishlist_api.client.models import Client


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('id', 'name', 'email',)


class ClientOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('id', 'name', 'email', 'created_at', 'updated_at')
