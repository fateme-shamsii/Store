from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from django.db import transaction
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True) # no white space here! ==> write_only=True
    password2 = serializers.CharField(write_only = True) # same
    email = serializers.EmailField(required=True)
    mobile_phone = serializers.CharField(write_only = True)
    name = serializers.CharField(write_only = True)

    class Meta:
        model = User
        # fields = [
        #     'name',
        #     'username',
        #     'email',
        #     'mobile_phone',
        #     'password',
        #     'password2'] # not like this, use tuple instead of list. 
        # do it like below
     fields = (
            'name', 'username', 'email', 'mobile_phone', 'password', 'password2'
     )

    def create(self,validated_data):
        name = validated_data.pop('name')
        mobile_phone = validated_data.pop('mobile_phone')
        validated_data.pop('password2')      
        with transaction.atomic():
            # too long line!
           # user = User.objects.create_user(username = validated_data['username'],email = validated_data['email'],password = validated_data['password'])

            # do it like this
            user = User.objects.create_user(
                username = validated_data['username'], email=validated_data['email'], password=validated_data['password']
            ) # space after comma, follow the pep8 rules my girl!

            Profile.objects.create(user = user , name = name,mobile_phone =mobile_phone) # wrong space again
        return user
    
    
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

        if len(value)!= 11:
            raise serializers.ValidationError("Mobile phone length is invalid.")

        if Profile.objects.filter(mobile_phone=value).exists():
            raise serializers.ValidationError("Mobile phone is already registered.")

        return value






        






