import pytest

from wishlist_api.client.models import Client


@pytest.mark.django_db
class TestClient:

    def test_should_display_email_when_str_client(self, add_one_client):
        client = Client.objects.get(pk=1)
        assert str(client) == "<Client {'id': 1, 'name': 'Kevin', 'email': 'kevin@test.com'}>"  # noqa

    def test_should_create_client(self):
        client = Client.objects.create(name='Arthur', email='arthur@test.com')
        assert client.name == 'Arthur'
        assert client.email == 'arthur@test.com'
