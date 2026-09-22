from rest_framework import serializers
from .models import Store


class StoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Store
        fields = (
            'id',
            'name',
            'description',
            'owner',
            'city',
            'status',       
            )
        read_only_fields = (
            'id',
            'owner',
            'status',
        )
