from rest_framework import serializers
from api.models import Festival, CustomUser
from djoser.serializers import UserCreateSerializer


class CustomUserSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'date_of_birth', 'country', 'gender']
        

class FestivalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Festival
        fields = ['id', 'name', 'info', 'website', 'lat', 'lon']

