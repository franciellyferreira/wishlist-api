import uuid

from django.http import Http404

from wishlist_api.wishlist.models import Wishlist


def get_item_wishlist(client_id: int, product_id: uuid.uuid4):
    try:
        return Wishlist.objects.filter(
            client_id=client_id,
            product_id=product_id
        )
    except Wishlist.DoesNotExist:
        raise Http404


def filter_items_wishlist_by_client(client_id: int):
    try:
        return Wishlist.objects.filter(client=client_id)
    except Wishlist.DoesNotExist:
        raise Http404
