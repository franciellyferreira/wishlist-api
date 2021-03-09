from django.conf.urls import url
from django.urls import include

urlpatterns = [
    url(r'^api/', include('wishlist_api.client.urls')),
    url(r'^api/', include('wishlist_api.wishlist.urls')),
]
