import uuid

import pytest

from wishlist_api.client.models import Client
from wishlist_api.wishlist.models import Wishlist


@pytest.fixture
def product_id():
    return uuid.UUID('75c5b2b6-d354-4b44-84a2-684431bed1ec')


@pytest.fixture
def client():
    return Client.objects.create(name='Kevin', email='kevin@test.com')


@pytest.fixture
def add_one_wishlist(client, product_id):
    Wishlist.objects.create(client=client, product_id=product_id)


@pytest.fixture
def add_multi_products_wishlist(client):
    Wishlist.objects.create(client=client, product_id=uuid.uuid4())
    Wishlist.objects.create(client=client, product_id=uuid.uuid4())
    Wishlist.objects.create(client=client, product_id=uuid.uuid4())
