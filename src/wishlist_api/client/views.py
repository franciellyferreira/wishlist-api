from django.http import Http404
from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.response import Response

from wishlist_api.client.models import Client
from wishlist_api.client.serializers import ClientSerializer
from wishlist_api.pagination import CustomPagination


class ClientListCreateView(ListCreateAPIView):

    serializer_class = ClientSerializer
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

        payload = {
            'status_code': status.HTTP_200_OK,
            'message': 'success',
            'data': data
        }

        return Response(payload)

    def post(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)

        if serializer.is_valid():
            client = serializer.save()
            serializer = ClientSerializer(client)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClientRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):

    serializer_class = ClientSerializer

    def get_object(self):
        try:
            return Client.objects.get(pk=self.kwargs['pk'])
        except Client.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        client = self.get_object()
        serializer = ClientSerializer(client)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        client = self.get_object()
        serializer = ClientSerializer(client, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        client = self.get_object()
        serializer = ClientSerializer(client, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        client = self.get_object()
        client.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
