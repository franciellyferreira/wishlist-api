from uuid import UUID

import pytest

from wishlist_api.client.models import Client
from wishlist_api.wishlist.models import Wishlist


@pytest.fixture
def client():
    return Client.objects.create(name='Kevin', email='kevin@test.com')


@pytest.fixture
def add_one_wishlist(client, product_id):
    Wishlist.objects.create(client=client, product_id=product_id)


@pytest.fixture
def add_multi_products_wishlist(client):
    Wishlist.objects.create(
        client=client,
        product_id=UUID('1bf0f365-fbdd-4e21-9786-da459d78dd1f')
    )
    Wishlist.objects.create(
        client=client,
        product_id=UUID('356eafd9-224a-d242-a3f2-e29b4270a927')
    )
    Wishlist.objects.create(
        client=client,
        product_id=UUID('212d0f07-8f56-0708-971c-41ee78aadf2b')
    )
