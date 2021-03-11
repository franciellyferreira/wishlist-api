from unittest import mock
from uuid import UUID

import pytest


@pytest.fixture
def product_id():
    return UUID('958ec015-cfcf-258d-c6df-1721de0ab6ea')


@pytest.fixture
def product_id_not_exists():
    return UUID('958ec015-cfcf-258d-c6df-1721de0ab000')


@pytest.fixture
def mock_paginate_queryset():
    with mock.patch(
        'wishlist_api.client.views.ClientListCreateView.paginate_queryset'
    ) as client:
        client.return_value = None
        yield client
