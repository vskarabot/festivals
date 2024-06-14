from django.http import JsonResponse
from .choices import COUNTRIES

from api.models import Festival, Post, Chat, Message
from api.serializers import FestivalSerializer, PostSerializer, ChatSerializer, MessageSerializer

from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter

from .pusher_client import pusher_client
from .scraper import scrape_hotels

# Create your views here.
def countries(request):
    return JsonResponse(dict(COUNTRIES))


class FestivalList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer

    filter_backends = [SearchFilter]
    search_fields = ['name']

    def perform_create(self, serializer):
        festival = serializer.save()
        festival.mods.add(self.request.user)


class FestivalDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer

    def perform_update(self, serializer):
        instance = serializer.instance
        user = self.request.user
        
        #
        if 'favourite' in self.request.data:
            if user in instance.favourite_by.filter(id=user.id):
                instance.favourite_by.remove(user)
            else:
                instance.favourite_by.add(user)
            instance.save()

        # EDIT - else it must be edit request, so check if user is mod
        else:
            if user in instance.mods.all():
                serializer.update(instance, serializer.validated_data)
            else:
                raise serializers.ValidationError('Only mods can change the festival')
            

# for hotels
class Hotels(generics.ListAPIView):
    def list(self, request, *args, **kwargs):
        
        # check if any important are missing
        required_params = ['place', 'checkin', 'checkout', 'adults']
        for param in required_params:
            if param not in request.query_params:
                raise serializers.ValidationError(f'Parameter "{param}" is missing!')
        
        # make url
        # place of festival (location would be better name)
        place = request.query_params.get('place')
        checkin = request.query_params.get('checkin')
        checkout = request.query_params.get('checkout')
        adults = request.query_params.get('adults')
        rooms = request.query_params.get('rooms', 1)
        min_ppn = request.query_params.get('min_ppn', 'min')
        max_ppn = request.query_params.get('max_ppn', 'max')
        # children = request.query_params.get('children', None) always 0
        #currency = request.query_params.get('currency', None)

        url = f"https://www.booking.com/searchresults.html?ss={place}&ssne={place}&ssne_untouched={place}&lang=en-us&sb=1&src_elem=sb&src=searchresults&checkin={checkin}&checkout={checkout}&group_adults={adults}&no_rooms={rooms}&group_children=0&selected_currency=EUR&soz=1&lang_changed=1&price%3DEUR-{min_ppn}-{max_ppn}-1"

        # Scrape hotels based on location
        hotels_data = scrape_hotels(url)
        return Response(hotels_data)



class PostList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = PostSerializer

    def get_queryset(self):
        query_params = self.request.query_params.get('festival') 
        if query_params:
            return Post.objects.filter(festival=query_params)
        return Post.objects.all()

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

    

# help method
def like_or_dislike(instance, user, action):
    if action == 'like':
        instance.post_disliked_by.remove(user)
        instance.post_liked_by.add(user) if user not in instance.post_liked_by.all() else instance.post_liked_by.remove(user)
    elif action == 'dislike':
        instance.post_liked_by.remove(user)
        instance.post_disliked_by.add(user) if user not in instance.post_disliked_by.all() else instance.post_disliked_by.remove(user)
    instance.save()


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = PostSerializer
    queryset = Post.objects.all()

    def perform_update(self, serializer):
        instance = serializer.instance
        user = self.request.user
        action = self.request.data.get('action')

        if action:
            like_or_dislike(instance, user, action)
            
        serializer.save()


class ChatList(generics.ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)

    serializer_class = ChatSerializer

    def get_queryset(self):
        festival = self.kwargs['pk']
        return Chat.objects.filter(festival=festival)
    
    def perform_create(self, serializer):
        festival_id = self.kwargs['pk']
        festival = Festival.objects.get(id=festival_id)
        serializer.save(festival=festival)
    


class MessageList(generics.ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)

    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    # check if chat is in the festival
    def get_queryset(self):
        try:
            chat = Chat.objects.get(id=self.kwargs['cpk'], festival=self.kwargs['pk'])
        except Chat.DoesNotExist:
            raise serializers.ValidationError('Chat does not exist')
        return Message.objects.filter(chat=chat)
    

    def perform_create(self, serializer):
        user = self.request.user
        chat_id = self.kwargs['cpk']
        chat = Chat.objects.get(id=chat_id)
        
        # save
        message = serializer.save(author=user, chat=chat)
        
        # send message to pusher to update frontend
        #### TODO well just exclude is_author field as it is calculated on frontend
        # probably like this
        data = serializer.data
        data.pop('is_author')
        pusher_client.trigger(f'chat-{message.chat.id}', 'new-message', data)