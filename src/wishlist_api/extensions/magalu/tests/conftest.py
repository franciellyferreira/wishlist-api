import pytest
from simple_settings import settings

API_URL = settings.API_MAGALU_PRODUCT['API_MAGALU_PRODUCT']['url']


@pytest.fixture
def api_magalu_response_payload():
    return {
        'price': 1149,
        'image': f'{API_URL}/images/958ec015-cfcf-258d-c6df-1721de0ab6ea.jpg',
        'brand': 'bébé confort',
        'id': '958ec015-cfcf-258d-c6df-1721de0ab6ea',
        'title': 'Moisés Dorel Windoo 1529'
    }


@pytest.fixture
def api_magalu_response_exception_payload():
    return {
        'error_message': (
            'Product 958ec015-cfcf-258d-c6df-1721de0ab000 not found'
        ),
        'code': 'not_found'
    }


@pytest.fixture
def product_id():
    return '958ec015-cfcf-258d-c6df-1721de0ab6ea'


@pytest.fixture
def product_id_not_exists():
    return '958ec015-cfcf-258d-c6df-1721de0ab000'
