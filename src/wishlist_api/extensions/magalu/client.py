import uuid
import structlog

import requests
from simple_settings import settings

from wishlist_api.extensions.magalu.exceptions import MagaluProductAPIException

logger = structlog.get_logger()

API_MAGALU_PRODUCT = settings.API_MAGALU_PRODUCT['API_MAGALU_PRODUCT']


def get_product_from_magalu(product_id: uuid.uuid4):

    try:
        api_url = API_MAGALU_PRODUCT['url']
        api_timeout = API_MAGALU_PRODUCT['timeout']

        url = f'{api_url}/api/product/{product_id}/'

        response = requests.get(
            url=url,
            timeout=api_timeout
        )

        response.raise_for_status()

        logger.info(
            'Product from Magalu successfully received',
            product_id=product_id
        )

        return response.json()
    except Exception as exception:
        raise MagaluProductAPIException() from exception
