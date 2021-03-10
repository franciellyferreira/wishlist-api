import json

import pytest
import responses
from rest_framework import status
from simple_settings import settings

from wishlist_api.extensions.magalu.client import get_product_from_magalu
from wishlist_api.extensions.magalu.exceptions import MagaluProductAPIException

API_URL = settings.API_MAGALU_PRODUCT['API_MAGALU_PRODUCT']['url']


class TestClient:

    def test_should_return_product_when_product_found_in_magalu(
        self,
        product_id,
        api_magalu_response_payload
    ):
        with responses.RequestsMock() as mock_response:
            request_url = f'{API_URL}/api/product/{product_id}/'

            mock_response.add(
                method=responses.GET,
                url=request_url,
                status=status.HTTP_200_OK,
                body=json.dumps(api_magalu_response_payload)
            )

            response = get_product_from_magalu(product_id=product_id)

        assert response == api_magalu_response_payload

    def test_should_return_exception_when_product_not_found_in_magalu(
        self,
        product_id_not_exists,
        api_magalu_response_exception_payload
    ):
        with responses.RequestsMock() as mock_response:
            request_url = f'{API_URL}/api/product/{product_id_not_exists}/'

            mock_response.add(
                method=responses.GET,
                url=request_url,
                status=status.HTTP_404_NOT_FOUND,
                body=json.dumps(api_magalu_response_exception_payload)
            )

            with pytest.raises(MagaluProductAPIException):
                get_product_from_magalu(product_id=product_id_not_exists)
