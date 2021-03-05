import pytest

from wishlist_api.client.models import Client

pytestmark = pytest.mark.django_db


class TestClient:

    def test_should_display_email_when_print_client(self):
        Client.objects.create(
            name='Franciélly',
            email='franciellydeveloper@gmail.com'
        )
        client = Client.objects.get(pk=1)

        assert str(client) == 'franciellydeveloper@gmail.com'

    def test_should_create_client(self):
        client = Client.objects.create(
            name='Franciélly',
            email='franciellydeveloper@gmail.com'
        )
        assert client.name == 'Franciélly'
