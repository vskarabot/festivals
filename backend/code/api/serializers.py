from rest_framework import serializers
from api.models import Festival, CustomUser, Post, Chat, Message
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
    def get_is_favourite(self, obj):
        user = self.context['request'].user
        return user in obj.favourite_by.all()
    
    def get_is_mod(self, obj):
        user = self.context['request'].user
        return user in obj.mods.all()


class PostSerializer(serializers.ModelSerializer):
    number_of_likes = serializers.SerializerMethodField()
    number_of_dislikes = serializers.SerializerMethodField()
    festival_name = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()
    can_delete = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 
            'title', 
            'time', 
            'text', 
            'label',  
            
            #'author', #-> not serialized, we can access it from the request
            'is_author', #-> serialized
            'username', #-> serialized
            'can_delete',
            'festival',
            'festival_name',

            #'post_liked_by',
            'number_of_likes',
            #'post_disliked_by',
            'number_of_dislikes',
        ]
    
    def get_number_of_likes(self, obj):
        return obj.post_liked_by.count()
    
    def get_number_of_dislikes(self, obj):
        return obj.post_disliked_by.count()
    
    def get_festival_name(self, obj):
        return obj.festival.name
    
    def get_is_author(self, obj):
        return self.context['request'].user == obj.author
    
    def get_can_delete(self, obj):
        return self.context['request'].user in obj.festival.mods.all()
    
    def get_username(self, obj):
        return obj.author.username


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['id', 'name']


class MessageSerializer(serializers.ModelSerializer):
    is_author = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'id', 
            'text', 
            'time', 
            'author', 
            'is_author'
        ]
        read_only_fields = ['author']

    def get_is_author(self, obj):
        return self.context['request'].user == obj.author