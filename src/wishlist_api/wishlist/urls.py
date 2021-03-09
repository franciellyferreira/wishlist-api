from django.urls import path

from wishlist_api.wishlist.views import (
    WishlistCreateView,
    WishlistDestroyView,
    WishlistListView
)

urlpatterns = [
    path(
        'wishlist/',
        WishlistCreateView.as_view(),
        name='wishlist-create'
    ),
    path(
        'wishlist/<int:pk>/',
        WishlistListView.as_view(),
        name='wishlist-list'
    ),
    path(
        'wishlist/<int:pk>/<str:product>/',
        WishlistDestroyView.as_view(),
        name='wishlist-destroy'
    )
]
