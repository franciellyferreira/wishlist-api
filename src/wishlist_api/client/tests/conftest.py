import pytest

from wishlist_api.client.models import Client


@pytest.fixture
def add_one_client():
    Client.objects.create(name='Kevin', email='kevin@test.com')


@pytest.fixture
def add_three_clients():
    Client.objects.create(name='Kevin', email='kevin@test.com')
    Client.objects.create(name='Bill', email='bill@test.com')
    Client.objects.create(name='William', email='william@test.com')


@pytest.fixture
def add_more_then_ten_clients():
    Client.objects.create(name='Kevin', email='kevin@test.com')
    Client.objects.create(name='Bill', email='bill@test.com')
    Client.objects.create(name='William', email='william@test.com')
    Client.objects.create(name='Monica', email='monica@test.com')
    Client.objects.create(name='Isabelle', email='isabelle@test.com')
    Client.objects.create(name='Larissa', email='larissa@test.com')
    Client.objects.create(name='Maria', email='maria@test.com')
    Client.objects.create(name='Jorge', email='jorge@test.com')
    Client.objects.create(name='Wilson', email='wilson@test.com')
    Client.objects.create(name='Cora', email='cora@test.com')
    Client.objects.create(name='Virginia', email='virginia@test.com')
