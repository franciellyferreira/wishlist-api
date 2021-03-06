from django.conf.urls import url
from django.urls import include


urlpatterns = [
    url(r'^wishlist/', include('wishlist_api.client.urls')),
]
