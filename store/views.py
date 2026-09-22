from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Store
from .serializers import StoreSerializer


class StoreListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stores = Store.objects.select_related('owner', 'city').filter(
            is_active=True
        )
        city_id = request.query_params.get('city')

        if city_id:
            stores = stores.filter(city_id=city_id)

        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = StoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=request.user)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )