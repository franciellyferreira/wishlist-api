import uuid
import structlog

import requests
from simple_settings import settings

from wishlist_api.extensions.magalu.exceptions import ProductAPIException

logger = structlog.get_logger()

API_PRODUCT_MAGALU = settings.API_PRODUCT_MAGALU['API_PRODUCT_MAGALU']


def get_product_from_magalu(product_id: uuid.uuid4):

    try:
        api_url = API_PRODUCT_MAGALU['url']
        api_timeout = API_PRODUCT_MAGALU['timeout']

        url = f'{api_url}/api/product/{product_id}/'

        response = requests.get(
            url=url,
            timeout=api_timeout
        )

        response.raise_for_status()

        logger.info(
            'Product from Magalu successfully received.',
            product_id=product_id
        )

        return response.json()
    except Exception as error:
        logger.error(
            'Fail to get product from Magalu.',
            product_id=product_id,
            exc_info=True
        )
        raise ProductAPIException() from error
