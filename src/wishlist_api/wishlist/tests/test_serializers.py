from decimal import Decimal

import pytest
from django.utils import timezone

from wishlist_api.extensions.magalu.models import Product
from wishlist_api.wishlist.serializers import (
    WishlistDescriptionOutputSerializer,
    WishlistOutputSerializer,
    WishlistSerializer
)


@pytest.mark.django_db
class TestWishlistSerializer:

    def test_should_return_wishlist_serializer(self, client, product_id):
        wishlist = {
            'client': client.id,
            'product_id': product_id
        }
        serializer = WishlistSerializer(data=wishlist)

        assert serializer.is_valid()
        assert serializer.errors == {}
        assert serializer.initial_data['client'] == 1
        assert serializer.initial_data['product_id'] == product_id


@pytest.mark.django_db
class TestWishlistOutputSerializer:

    def test_should_return_wishlist_output_serializer(
        self,
        client,
        product_id
    ):
        now = timezone.now()

        wishlist = {
            'client': client.id,
            'product_id': product_id,
            'created_at': now
        }
        serializer_output = WishlistOutputSerializer(data=wishlist)

        assert serializer_output.is_valid()
        assert serializer_output.errors == {}
        assert serializer_output.initial_data['client'] == 1
        assert serializer_output.initial_data['product_id'] == product_id
        assert serializer_output.initial_data['created_at'] == now


@pytest.mark.django_db
class TestWishlistDescriptionOutputSerializer:

    def test_should_return_wishlist_description_output_serializer(
        self,
        product_id
    ):
        product = Product(
            id=product_id,
            title='geladeira',
            image='http://url_api/imagem.jpg',
            price=Decimal(1300),
            brand='eletrolux'
        )
        serializer_output = WishlistDescriptionOutputSerializer(
            data=product.as_dict()
        )

        assert serializer_output.is_valid()
        assert serializer_output.errors == {}
        assert serializer_output.initial_data['id'] == product_id
        assert serializer_output.initial_data['title'] == 'geladeira'
        assert serializer_output.initial_data['image'] == (
            'http://url_api/imagem.jpg'
        )
        assert serializer_output.initial_data['price'] == Decimal(1300)
        assert serializer_output.initial_data['brand'] == 'eletrolux'
