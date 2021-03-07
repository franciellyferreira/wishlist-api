from rest_framework import serializers

from wishlist_api.wishlist.models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wishlist
        fields = ('client', 'product_id')


class WishlistOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wishlist
        fields = ('id', 'client', 'product_id', 'created_at')
