from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BrandSerializer
from .models import Brand

class BrandListView(APIView):
    def get(self, request):
        brands = Brand.objects.filter(is_active=True)
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)

