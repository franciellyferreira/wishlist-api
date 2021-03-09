from rest_framework import serializers

from wishlist_api.wishlist.models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wishlist
        fields = ('client', 'product_id')


class WishlistOutputSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wishlist
        fields = ('client', 'product_id', 'created_at')


class WishlistDescriptionOutputSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(default='')
    price = serializers.FloatField(default=0.0)
    title = serializers.CharField(max_length=100, default='')
    image = serializers.CharField(max_length=200, default='')
    brand = serializers.CharField(max_length=50, default='')

    class Meta:
        model = Wishlist
        fields = ('id', 'title', 'image', 'price', 'brand')
