import pytest
from django.utils import timezone

from wishlist_api.client.serializers import (
    ClientOutputSerializer,
    ClientSerializer
)


@pytest.mark.django_db
class TestClientSerializer:

    def test_should_create_client_serializer(self):
        client = {
            'name': 'test',
            'email': 'test@test.com'
        }
        serializer = ClientSerializer(data=client)

        assert serializer.is_valid()
        assert serializer.errors == {}
        assert serializer.initial_data['name'] == 'test'
        assert serializer.initial_data['email'] == 'test@test.com'


@pytest.mark.django_db
class TestClientOutputSerializer:

    def test_should_create_client_output_serializer(self):
        now = timezone.now()

        client = {
            'id': 10,
            'name': 'test',
            'email': 'test@test.com',
            'created_at': now,
            'updated_at': now
        }
        serializer_output = ClientOutputSerializer(data=client)

        assert serializer_output.is_valid()
        assert serializer_output.errors == {}
        assert serializer_output.initial_data['id'] == 10
        assert serializer_output.initial_data['name'] == 'test'
        assert serializer_output.initial_data['email'] == 'test@test.com'
        assert serializer_output.initial_data['created_at'] == now
        assert serializer_output.initial_data['updated_at'] == now
