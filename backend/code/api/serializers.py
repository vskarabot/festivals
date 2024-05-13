from rest_framework import serializers
from api.models import Festival, CustomUser
from djoser.serializers import UserCreateSerializer


class CustomUserSerializer(UserCreateSerializer):
    festivals = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    favourite_festivals = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 
                  'first_name', 
                  'last_name', 
                  'username', 
                  'email', 
                  'password', 
                  'date_of_birth', 
                  'country', 
                  'gender',
                  
                  'festivals',
                  'favourite_festivals']
        

class FestivalSerializer(serializers.ModelSerializer):
    is_favourite = serializers.SerializerMethodField()
    is_mod = serializers.SerializerMethodField()

    class Meta:
        model = Festival
        fields = ['id', 
                  'name', 
                  'info', 
                  'website', 
                  'lat', 
                  'lon', 
                  
                  'is_mod',
                  'is_favourite']
        
    # attributes are also accessible if they are not seriialized (from model) - mods and favourite_by
    # we can use them to check if the user is a mod or if the user has favourited the festival without actually sending it over the wire
    def create(self, validated_data):
        user = self.context['request'].user
        festival = super().create(validated_data)
        festival.mods.add(user)
        return festival

    def update(self, instance, validated_data):
        user = self.context['request'].user

        # FAVOURITE - if favourite is sent in request don't check if user is mod
        if 'favourite' in self.context['request'].data:
            if user in instance.favourite_by.filter(id=user.id):
                instance.favourite_by.remove(user)
            else:
                instance.favourite_by.add(user)
        # EDIT - else it must be edit request, so check if user is mod
        else:
            if user in instance.mods.all():
                instance = super().update(instance, validated_data)
            else:
                raise serializers.ValidationError('Only mods can change the festival')

        return instance
    
    
    def get_is_favourite(self, obj):
        user = self.context['request'].user
        return user in obj.favourite_by.all()
    
    def get_is_mod(self, obj):
        user = self.context['request'].user
        return user in obj.mods.all()
