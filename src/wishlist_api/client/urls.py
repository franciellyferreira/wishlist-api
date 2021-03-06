from django.conf.urls import url
from django.urls import path

from wishlist_api.client.views import (
    ClientListCreateView,
    ClientRetrieveUpdateDestroyView
)


urlpatterns = [
    path(
        'client/',
        ClientListCreateView.as_view(),
        name='client-list-create'
    ),
    path(
        'client/<str:pk>/',
        ClientRetrieveUpdateDestroyView.as_view(),
        name='client-retrieve-update-destroy'
    )
]
