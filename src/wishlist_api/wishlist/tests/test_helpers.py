import pytest

from wishlist_api.wishlist.helpers import (
    filter_items_wishlist_by_client,
    get_item_wishlist
)


@pytest.mark.django_db
class TestHelpers:

    def test_should_return_wishlist_by_client_and_product(
        self,
        add_one_wishlist,
        product_id
    ):
        wishlist = get_item_wishlist(client_id=1, product_id=product_id)
        assert wishlist[0].client.id == 1
        assert wishlist[0].product_id == product_id
        assert len(wishlist) == 1

    def test_should_return_wishlist_by_client(
        self,
        add_multi_products_wishlist
    ):
        wishlists = filter_items_wishlist_by_client(client_id=1)
        assert len(wishlists) == 3
