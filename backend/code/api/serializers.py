from datetime import datetime, timedelta
from rest_framework import serializers
from api.models import  Festival, CustomUser, Notification, Post, Chat, Message, Comment
from djoser.serializers import UserCreateSerializer
from django.db.models import Count


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
    num_favourites = serializers.SerializerMethodField()

    class Meta:
        model = Festival
        fields = ['id', 
                  'name', 
                  'info', 
                  'website', 
                  'lat', 
                  'lon',
                  'date_start',
                  'date_end',
                  'img',
                  
                  'is_mod',
                  'is_favourite',
                  'num_favourites']
        
    # attributes are also accessible if they are not seriialized (from model) - mods and favourite_by 
    def get_is_favourite(self, obj):
        user = self.context['request'].user
        return user in obj.favourite_by.all()
    
    def get_is_mod(self, obj):
        user = self.context['request'].user
        return user in obj.mods.all()
    
    def get_num_favourites(self, obj):
        return len(obj.favourite_by.all())


# method that returns time as when it was published
# used in post and comment serializers
def readable_time(obj):
    now = datetime.now(obj.time.tzinfo)
    difference = now - obj.time

    if difference < timedelta(seconds=60):
        return "now"
    elif difference < timedelta(minutes=60):
        minutes = difference.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    elif difference < timedelta(hours=24):
        hours = difference.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif difference < timedelta(days=30):
        days = difference.days
        return f"{days} day{'s' if days > 1 else ''} ago"
    elif difference < timedelta(days=365):
        months = difference.days // 30
        return f"{months} month{'s' if months > 1 else ''} ago"
    else:
        years = difference.days // 365
        return f"{years} year{'s' if years > 1 else ''} ago"

class PostSerializer(serializers.ModelSerializer):
    number_of_likes = serializers.SerializerMethodField()
    number_of_dislikes = serializers.SerializerMethodField()
    festival_name = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()
    can_delete = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    time_string = serializers.SerializerMethodField()
    user_likes = serializers.SerializerMethodField()
    user_dislikes = serializers.SerializerMethodField()
    number_of_comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = [
            'id', 
            'title', 
            'time',
            # look method below
            'time_string',
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
            'number_of_comments',
            'user_likes',
            'user_dislikes',
            'edited'
        ]
    
    def get_number_of_likes(self, obj):
        return obj.post_liked_by.count()
    
    def get_number_of_dislikes(self, obj):
        return obj.post_disliked_by.count()
    
    def get_number_of_comments(self, obj):
        return obj.post_comments.count()
    
    def get_festival_name(self, obj):
        return obj.festival.name
    
    def get_is_author(self, obj):
        return self.context['request'].user == obj.author
    
    def get_can_delete(self, obj):
        return self.context['request'].user in obj.festival.mods.all()
    
    def get_username(self, obj):
        return obj.author.username
    
    def get_time_string(self, obj):
        return readable_time(obj)
    
    def get_user_likes(self, obj):
        return self.context['request'].user in obj.post_liked_by.all()
    
    def get_user_dislikes(self, obj):
        return self.context['request'].user in obj.post_disliked_by.all()
    

class CommentSerializer(serializers.ModelSerializer):
    child_comments = serializers.SerializerMethodField()
    time_string = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    is_author = serializers.SerializerMethodField()

    number_of_likes = serializers.SerializerMethodField()
    number_of_dislikes = serializers.SerializerMethodField()
    user_likes = serializers.SerializerMethodField()
    user_dislikes = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'time', 'time_string', 'text', 'deleted',
                  'number_of_likes', 'number_of_dislikes', 'user_likes', 'user_dislikes',
                #'author',
                'is_author','username', 'post', 'parent', 'child_comments']

    def get_child_comments(self, obj):
        #child_comments = obj.child_comments.all()
        
        # important to pass context as it's not passed in recursion for some reason
        #return CommentSerializer(child_comments, context=self.context, many=True).data
        sort = self.context['request'].query_params.get('sort')
        if sort == 'Top':
            child_comments = obj.child_comments.annotate(top=Count('comment_liked_by')).order_by('-top')
        else:
            child_comments = obj.child_comments.all()
        return CommentSerializer(child_comments, context=self.context, many=True).data

    def get_time_string(self, obj):
        return readable_time(obj)
    
    def get_username(self, obj):
        return obj.author.username
    
    def get_is_author(self, obj):
        return self.context['request'].user == obj.author
    
    def get_number_of_likes(self, obj):
        return obj.comment_liked_by.count()
    
    def get_number_of_dislikes(self, obj):
        return obj.comment_disliked_by.count()
    
    def get_user_likes(self, obj):
        return self.context['request'].user in obj.comment_liked_by.all()
    
    def get_user_dislikes(self, obj):
        return self.context['request'].user in obj.comment_disliked_by.all()
    

    

class ChatSerializer(serializers.ModelSerializer):
    notify_user = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = ['id', 'name', 'notify_user', 'notified_users']

    def get_notify_user(self, obj):
        return self.context['request'].user in obj.notified_users.all()

class MessageSerializer(serializers.ModelSerializer):
    time_string = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = [
            'id', 
            'text', 
            'time',
            'time_string', 
            'author', 
            'username'
        ]
        read_only_fields = ['author']
    
    def get_time_string(self, obj):
        return readable_time(obj)
    
    def get_username(self, obj):
        return obj.author.username

def readable_time_notifications(obj):
    now = datetime.now(obj.timestamp.tzinfo)
    difference = now - obj.timestamp

    if difference < timedelta(seconds=60):
        return "now"
    elif difference < timedelta(minutes=60):
        minutes = difference.seconds // 60
        return f"{minutes}min"
    elif difference < timedelta(hours=24):
        hours = difference.seconds // 3600
        return f"{hours}h"
    elif difference < timedelta(days=30):
        days = difference.days
        return f"{days} day{'s' if days > 1 else ''}"
    else:
        return "Older"
    
class NotificationSerializer(serializers.ModelSerializer):
    message_text = serializers.CharField(source='message.text', read_only=True)
    message_username = serializers.CharField(source='message.author.username', read_only=True)
    festival = serializers.IntegerField(source='chat.festival.id', read_only=True)
    chat_name = serializers.CharField(source='chat.name', read_only=True)
    time_string = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'timestamp', 'read', 'user', 'chat', 'message', 'festival', 'message_username', 'message_text', 'chat_name', 'time_string']

    def get_time_string(self, obj):
        return readable_time_notifications(obj)