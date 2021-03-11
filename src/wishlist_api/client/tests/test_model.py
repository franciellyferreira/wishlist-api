import pytest

from wishlist_api.client.models import Client


@pytest.mark.django_db
class TestClient:

    def test_should_create_client(self):
        client = Client.objects.create(name='Arthur', email='arthur@test.com')
        assert client.name == 'Arthur'
        assert client.email == 'arthur@test.com'
        assert client.as_dict() != {}
