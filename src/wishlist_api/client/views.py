from typing import Any

import structlog
from oauth2_provider.contrib.rest_framework import (
    OAuth2Authentication,
    TokenHasReadWriteScope
)
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.response import Response

from wishlist_api.client.helpers import get_client, get_all_clients
from wishlist_api.client.serializers import (
    ClientOutputSerializer,
    ClientSerializer
)
from wishlist_api.pagination import CustomPagination

logger = structlog.getLogger()


class ClientListCreateView(ListCreateAPIView):

    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [TokenHasReadWriteScope]
    serializer_class = ClientOutputSerializer
    pagination_class = CustomPagination

    queryset = get_all_clients()

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
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )

        logger.warning('Fail to created client', client=request.data)
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ClientRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):

    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [TokenHasReadWriteScope]
    serializer_class = ClientSerializer

    def _update_client(
            self,
            client_id: int,
            request: Any,
            partial: bool = False
    ) -> Response:
        client = get_client(pk=client_id)
        serializer = ClientSerializer(
            client,
            data=request.data,
            partial=partial
        )
        if serializer.is_valid():
            serializer.save()
            logger.info(
                'Client update with success',
                client=request.data,
                partial=partial
            )
            return Response(
                data=serializer.data,
                status=status.HTTP_204_NO_CONTENT
            )

        logger.info(
            'Fail to update why client data is invalid.',
            client=request.data,
            partial=partial
        )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def get(self, request, *args, **kwargs):
        client_id = self.kwargs['pk']
        client = get_client(pk=client_id)
        serializer = ClientOutputSerializer(client)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        client_id = self.kwargs['pk']
        return self._update_client(client_id=client_id, request=request)

    def patch(self, request, *args, **kwargs):
        client_id = self.kwargs['pk']
        return self._update_client(
            client_id=client_id,
            request=request,
            partial=True
        )

    def delete(self, request, *args, **kwargs):
        client_id = self.kwargs['pk']
        client = get_client(pk=client_id)
        client.delete()
        logger.info('Client deleted with success', client=request.data)
        return Response(status=status.HTTP_204_NO_CONTENT)
