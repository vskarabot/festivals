from rest_framework import serializers
from api.models import Festival, CustomUser
from djoser.serializers import UserCreateSerializer


class CustomUserSerializer(UserCreateSerializer):
    festivals = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

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
                  
                  'festivals']
        

class FestivalSerializer(serializers.ModelSerializer):
    mods = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Festival
        fields = ['id', 
                  'name', 
                  'info', 
                  'website', 
                  'lat', 
                  'lon', 
                  
                  'mods']
        
    
    # only mods can change
    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user in instance.mods.all():
            return super().update(instance, validated_data)
        else:
            raise serializers.ValidationError('Only mods can change the festival')

