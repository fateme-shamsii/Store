from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer,LoginSerializer



class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "message": "You have been registered successfully",
            "token": token.key,
            "user": {"username": user.username, "email": user.email,}
        }, status=status.HTTP_201_CREATED)


class LoginUserView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        token, created = Token.objects.get_or_create(user=user)

        return Response({
            "message": "You have been logged successfully",
            "token": token.key,
            "user_info":{"username": user.username, "email": user.email,}
        }, status=status.HTTP_200_OK)


class LogOutUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()

        return Response(
            {
                "message": "You have been logged out successfully."
            },
            status=status.HTTP_200_OK,
        )


