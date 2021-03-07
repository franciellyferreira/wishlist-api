from django.urls import path

from wishlist_api.wishlist.views import WishlistListCreateView

urlpatterns = [
    path(
        'wishlist/',
        WishlistListCreateView.as_view(),
        name='wishlist-list-create'
    )
]
