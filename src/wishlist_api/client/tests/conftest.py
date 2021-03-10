import pytest

from wishlist_api.client.models import Client


@pytest.fixture
def add_one_client():
    Client.objects.create(name='Kevin', email='kevin@test.com')


@pytest.fixture
def add_multi_clients():
    Client.objects.create(name='Kevin', email='kevin@test.com')
    Client.objects.create(name='Bill', email='bill@test.com')
    Client.objects.create(name='William', email='william@test.com')
