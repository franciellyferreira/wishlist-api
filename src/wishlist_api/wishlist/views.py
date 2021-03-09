import structlog
from django.http import Http404
from rest_framework import status
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView
from rest_framework.response import Response

from wishlist_api.client.helpers import get_client
from wishlist_api.extensions.magalu.client import get_product_from_magalu
from wishlist_api.extensions.magalu.exceptions import MagaluProductAPIException
from wishlist_api.extensions.magalu.models import Product
from wishlist_api.pagination import CustomPagination
from wishlist_api.wishlist.helpers import (
    filter_items_wishlist_by_client,
    get_item_wishlist
)
from wishlist_api.wishlist.models import Wishlist
from wishlist_api.wishlist.serializers import (
    WishlistDescriptionOutputSerializer,
    WishlistOutputSerializer,
    WishlistSerializer
)

logger = structlog.getLogger()


class WishlistCreateView(CreateAPIView):

    def post(self, request, *args, **kwargs):
        client_id = request.data['client']
        product_id = request.data['product_id']

        try:
            get_product_from_magalu(product_id=product_id)
        except MagaluProductAPIException:
            logger.error(
                'Fail during request to Magalu',
                product_id=product_id,
                exc_info=True
            )
            return Response(
                {'product_id': 'Not found in Magalu'},
                status=status.HTTP_404_NOT_FOUND
            )

        wishlist = get_item_wishlist(
            client_id=client_id,
            product_id=product_id
        )
        if not wishlist:
            serializer = WishlistSerializer(data=request.data)
            if serializer.is_valid():
                wishlist = serializer.save()
                serializer = WishlistOutputSerializer(wishlist)
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
            {'product_id': 'Already exists in wishlist'},
            status=status.HTTP_404_NOT_FOUND
        )


class WishlistListView(ListAPIView):

    serializer_class = WishlistDescriptionOutputSerializer
    pagination_class = CustomPagination
    queryset = Wishlist.objects.all().order_by('name')

    def get(self, request, *args, **kwargs):
        product_list = []
        client_id = self.kwargs['pk']

        try:
            get_client(pk=client_id)
        except Http404:
            return Response(
                {'client_id': 'Client not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        items = filter_items_wishlist_by_client(client_id=client_id)
        for item in items:
            magalu_product = get_product_from_magalu(item.product_id)
            product = Product(
                id=magalu_product['id'],
                title=magalu_product['title'],
                image=magalu_product['image'],
                price=magalu_product['price'],
                brand=magalu_product['brand']
            )
            product_list.append(product)

        queryset = self.filter_queryset(product_list)
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
