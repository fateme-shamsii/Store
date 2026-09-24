from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import CreateOrderSerializer,OrderSerializer
from .models import Order
from .services import OrderService

class OrderListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(
            user=request.user,
        ).prefetch_related(
            'items',
            'items_advertisement'
        ).order_by('-created_at')

        serializer = OrderSerializer(orders, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order = OrderService.create_order(
            user=request.user,
            items=serializer.validated_data['items'],
        )

        response_serializer = OrderSerializer(order)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )

