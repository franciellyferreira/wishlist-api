import uuid

from wishlist_api.wishlist.models import Wishlist


def get_item_wishlist(client_id: int, product_id: uuid.uuid4):
    return Wishlist.objects.filter(
        client_id=client_id,
        product_id=product_id
    )


def filter_items_wishlist_by_client(client_id: int):
    return Wishlist.objects.filter(client=client_id)
