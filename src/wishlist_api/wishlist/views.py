import structlog

from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.response import Response

from wishlist_api.extensions.products.client import get_product_from_magalu
from wishlist_api.pagination import CustomPagination
from wishlist_api.wishlist.helpers import (
    get_item_wishlist,
    filter_items_wishlist_by_client
)
from wishlist_api.wishlist.models import Wishlist
from wishlist_api.wishlist.serializers import (
    WishlistSerializer,
    WishlistOutputSerializer
)

logger = structlog.getLogger()


class WishlistCreateView(CreateAPIView):

    def post(self, request, *args, **kwargs):

        product_exists = True
        client_id = request.data['client']
        product_id = request.data['product_id']

        try:
            get_product_from_magalu(product_id=product_id)
        except Exception:
            product_exists = False

        wishlist = get_item_wishlist(
            client_id=client_id,
            product_id=product_id
        )

        if product_exists and not wishlist:
            serializer = WishlistSerializer(data=request.data)

            if serializer.is_valid():
                wishlist = serializer.save()
                serializer = WishlistSerializer(wishlist)
                logger.info('Product added in wishlist', data=request.data)
                return Response(
                    data=serializer.data,
                    status=status.HTTP_201_CREATED
                )
            logger.warning('Fail added product in wishlist', data=request.data)
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            data={
                'message': f'Product {product_id} not exists in Magalu '
                'or already exists in wishlist.'
            },
            status=status.HTTP_404_NOT_FOUND
        )


class WishlistListView(ListAPIView):

    serializer_class = WishlistOutputSerializer
    pagination_class = CustomPagination
    queryset = Wishlist.objects.all().order_by('name')

    def get(self, request, *args, **kwargs):
        client_id = self.kwargs['pk']
        queryset = self.filter_queryset(
            filter_items_wishlist_by_client(client_id=client_id)
        )
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

        return Response(data=data, status=status.HTTP_200_OK)


class WishlistDestroyView(DestroyAPIView):

    def delete(self, request, *args, **kwargs):
        client_id = self.kwargs['pk']
        product_id = self.kwargs['product']

        items = get_item_wishlist(
            client_id=client_id,
            product_id=product_id
        )
        items.delete()

        logger.info(
            'Deleted item from wishlist with success',
            client=request.data
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
