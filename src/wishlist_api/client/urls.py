from django.conf.urls import url

from wishlist_api.client import views


urlpatterns = [
    url(r'^$', views.ClientList.as_view()),
]
