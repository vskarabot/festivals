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
        
    
    # could be implemented in permissions but it's easier to do it here as we are validating data before updating
    # deserialize and update only if user is a mod; if not return an error
    # if user on frontend access via link he wont be able to change the festival
    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user in instance.mods.all():
            return super().update(instance, validated_data)
        else:
            raise serializers.ValidationError('Only mods can change the festival')

