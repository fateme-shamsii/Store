from rest_framework.views import APIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token


class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data = request.data) #space
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)
        # return Response({
        #     "message": "You have been registered successfully",
        #     "token": token.key,
        #     "user": {
        #         "username": user.username,
        #         "email": user.email,
        #     }
        # }, status=status.HTTP_201_CREATED)
         return Response({
            "message": "You have been registered successfully", "token": token.key,
            "user": {"username": user.username, "email": user.email}
        }, status=status.HTTP_201_CREATED)


        
    

