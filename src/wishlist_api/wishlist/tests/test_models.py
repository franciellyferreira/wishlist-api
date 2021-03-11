import pytest

from wishlist_api.wishlist.models import Wishlist


@pytest.mark.django_db
class TestClient:

    def test_should_create_wishlist(self, client, product_id):
        wishlist = Wishlist.objects.create(
            client=client,
            product_id=product_id
        )
        assert wishlist.client.id == 1
        assert wishlist.product_id == product_id
        assert wishlist.as_dict() != {}
