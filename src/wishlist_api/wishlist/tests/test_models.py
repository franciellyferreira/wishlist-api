import pytest

from wishlist_api.wishlist.models import Wishlist


@pytest.mark.django_db
class TestClient:

    def test_should_display_object_wishlist_when_print_wishlist(
        self,
        add_one_wishlist,
        product_id
    ):
        wishlist = Wishlist.objects.get(client_id=1, product_id=product_id)
        assert str(wishlist) == "<Wishlist {'id': 1, 'client_id': 1, " \
            "'product_id': UUID('75c5b2b6-d354-4b44-84a2-684431bed1ec')}>"

    def test_should_create_wishlist(self, client, product_id):
        wishlist = Wishlist.objects.create(
            client=client,
            product_id=product_id
        )
        assert wishlist.client.id == 1
        assert wishlist.product_id == product_id
