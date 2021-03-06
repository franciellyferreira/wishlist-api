from http import HTTPStatus

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from wishlist_api.client.models import Client
from wishlist_api.client.serializers import ClientSerializer
from wishlist_api.pagination import CustomPagination


class ClientList(GenericAPIView):
    serializer_class = ClientSerializer
    pagination_class = CustomPagination
    queryset = Client.objects.all().order_by('name')

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

        payload = {
            'status_code': HTTPStatus.OK.value,
            'message': 'success',
            'data': data
        }

        return Response(payload)
