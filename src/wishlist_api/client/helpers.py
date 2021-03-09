from django.http import Http404

from wishlist_api.client.models import Client


def get_client(pk: int) -> Client:
    try:
        return Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        raise Http404


def get_all_clients():
    return Client.objects.all().order_by('name')
