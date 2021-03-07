import structlog

from django.http import Http404
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.response import Response

from wishlist_api.client.helpers import get_client
from wishlist_api.client.models import Client
from wishlist_api.client.serializers import (
    ClientSerializer,
    ClientOutputSerializer
)
from wishlist_api.pagination import CustomPagination

logger = structlog.getLogger()


class ClientListCreateView(ListCreateAPIView):

    serializer_class = ClientOutputSerializer
    pagination_class = CustomPagination
    queryset = Client.objects.all().order_by('name')

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

        return Response(data=data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)

        if serializer.is_valid():
            client = serializer.save()
            serializer = ClientOutputSerializer(client)
            logger.info('Client created with success', client=request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.warning('Fail to created client', client=request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):

    serializer_class = ClientSerializer

    def get(self, request, *args, **kwargs):
        client_id = self.kwargs['pk']
        client = get_client(pk=client_id)
        serializer = ClientOutputSerializer(client)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        client_id = self.kwargs['pk']
        client = get_client(pk=client_id)
        serializer = ClientSerializer(client, data=request.data)

        if serializer.is_valid():
            serializer.save()
            logger.info('Client updated with success', client=request.data)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        logger.warning('Fail to updated client', client=request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        client_id = self.kwargs['pk']
        client = get_client(pk=client_id)
        serializer = ClientSerializer(client, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            logger.info('Client patched with success', client=request.data)
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        logger.warning('Fail to patched client', client=request.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        client_id = self.kwargs['pk']
        client = get_client(pk=client_id)
        client.delete()
        logger.info('Client deleted with success', client=request.data)
        return Response(status=status.HTTP_204_NO_CONTENT)
