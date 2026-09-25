from rest_framework import serializers

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import authenticate

from .models import Profile
from .services import UserService

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    mobile_phone = serializers.CharField(write_only=True)
    name = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('name', 'username', 'email', 'mobile_phone', 'password', 'password2')

    def create(self,validated_data):
        name = validated_data.pop('name')
        mobile_phone = validated_data.pop('mobile_phone')
        validated_data.pop('password2')   
           
        return UserService.create_user_with_profile(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            name=name,
            mobile_phone=mobile_phone,
        )
    
    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({'password': "passwords don't match"})
        return attrs
    
    def validate_username(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Username is required.")
        value = value.strip()

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username is already taken.")

        return value
    
    def validate_email(self, value):
        value = value.strip().lower()

        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email is already registered.")

        return value

    def validate_mobile_phone(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Mobile phone is required.")

        value = value.strip()

        if not value.isdigit():
            raise serializers.ValidationError("Mobile phone must contain only digits.")

        if len(value) != 11:
            raise serializers.ValidationError("Mobile phone length is invalid.")

        if Profile.objects.filter(mobile_phone=value).exists():
            raise serializers.ValidationError("Mobile phone is already registered.")

        return value


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self,attr):
        username = attr.get('username')
        password = attr.get('password')

        user = authenticate(
            username = username,
            password = password,
        )
        if user is None:
            raise serializers.ValidationError("password or username is not true")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        attr['user'] = user
        return attr
        





        






