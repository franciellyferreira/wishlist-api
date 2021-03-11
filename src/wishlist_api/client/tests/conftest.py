from unittest import mock

import pytest

from wishlist_api.client.models import Client
from wishlist_api.client.views import logger


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


@pytest.fixture
def mock_logger_info():
    with mock.patch.object(logger, 'info') as mock_logger_info:
        yield mock_logger_info


@pytest.fixture
def mock_logger_warning():
    with mock.patch.object(logger, 'warning') as mock_logger_warning:
        yield mock_logger_warning


@pytest.fixture
def mock_paginate_queryset():
    with mock.patch(
        'wishlist_api.client.views.ClientListCreateView.paginate_queryset'
    ) as client:
        client.return_value = None
        yield client
