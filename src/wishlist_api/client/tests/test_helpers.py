import pytest
from django.http import Http404

from wishlist_api.client.helpers import get_all_clients, get_client


@pytest.mark.django_db
class TestHelpers:

    def test_should_return_one_client_when_client_exists(self, add_one_client):
        client = get_client(pk=1)
        assert client.name == 'Kevin'

    def test_should_return_error_404_when_client_not_exists(
        self,
        add_one_client
    ):
        with pytest.raises(Http404):
            get_client(pk=2)

    def test_should_return_all_clients(self, add_three_clients):
        clients = get_all_clients()
        assert len(clients) == 3
