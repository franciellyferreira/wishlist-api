from django.http import Http404

from wishlist_api.client.models import Client


def get_client(pk):
    try:
        return Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        raise Http404
