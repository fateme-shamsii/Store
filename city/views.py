from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import CitySerializer
from .models import City



# Create your views here.

class ListCityView(APIView):

    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)
