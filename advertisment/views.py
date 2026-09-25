from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Advertisement
from .serializers import (AdvertisementCreateSerializer, AdvertisementListSerializer)


class AdvertisementListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        advertisements = Advertisement.objects.select_related('store', 'category', 'brand',
        ).filter(deleted_at__isnull=True,)
        serializer = AdvertisementListSerializer(advertisements, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = AdvertisementCreateSerializer(data=request.data, context={'request': request},)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)