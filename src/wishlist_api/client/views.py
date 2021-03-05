from rest_framework.response import Response
from rest_framework.views import APIView

from wishlist_api.client.models import Client
from wishlist_api.client.serializers import ClientSerializer


class ClientList(APIView):

    def get(self, request, format=None):
        clients = Client.objects.all()
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)
