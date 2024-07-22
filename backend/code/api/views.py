from django.http import JsonResponse
from django.http import Http404
from .choices import COUNTRIES

from django.db.models import Count, Case, When, FloatField, Value, F, Q

from api.models import Festival, Notification, Post, Chat, Message, Comment
from api.serializers import FestivalSerializer, NotificationSerializer, PostSerializer, ChatSerializer, MessageSerializer, CommentSerializer

from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

from .pusher_client import pusher_client
from .scraper import scrape_hotels

from datetime import date

# Create your views here.
def countries(request):
    return JsonResponse(dict(COUNTRIES))

class FestivalList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    #queryset = Festival.objects.all()
    serializer_class = FestivalSerializer

    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_queryset(self):
        sort_by = self.request.query_params.get('sort')
        upcoming = self.request.query_params.get('upcoming')
        favourites = self.request.query_params.get('favourites')

        # TODO : Date, nearby
        queryset = Festival.objects.all()
        user = self.request.user
        if sort_by == 'Popularity':
            queryset = queryset.annotate(most_popular=Count('favourite_by')).all().order_by('-most_popular')
        else:
            queryset = queryset.order_by(
                F('date_start').desc(nulls_last=True)
            )
        if favourites:
            queryset = queryset.filter(favourite_by=user)
        if upcoming:
            queryset = queryset.exclude(date_start__isnull=True)
            queryset = queryset.filter(Q(date_start__gte=date.today()) | Q(date_end__gte=date.today()))
        return queryset
    

    def perform_create(self, serializer):
        festival = serializer.save()
        festival.mods.add(self.request.user)


class FestivalDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    #queryset = Festival.objects.all()
    serializer_class = FestivalSerializer

    def get_object(self):
        try:
            return Festival.objects.get(id=self.kwargs['pk'])
        except Festival.DoesNotExist:
            raise Http404("Festival does not exist")
    
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
        required_params = ['lat', 'lon', 'checkin', 'checkout', 'adults', 'order']
        for param in required_params:
            if param not in request.query_params:
                raise serializers.ValidationError(f'Parameter "{param}" is missing!')
        
        # make url
        # place of festival (location would be better name)
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        checkin = request.query_params.get('checkin')
        checkout = request.query_params.get('checkout')
        adults = request.query_params.get('adults')
        rooms = request.query_params.get('rooms', 1)
        # min not gona be used (only max will be)
        max_ppn = request.query_params.get('maxPricePerNight', 'max')
        order = request.query_params.get('order')
        # children = request.query_params.get('children', None) always 0
        #currency = request.query_params.get('currency', None)

        #url = f"https://www.booking.com/searchresults.html?ss={place}&ssne={place}&ssne_untouched={place}&lang=en-us&sb=1&src_elem=sb&src=searchresults&checkin={checkin}&checkout={checkout}&group_adults={adults}&no_rooms={rooms}&group_children=0&selected_currency=EUR&soz=1&lang_changed=1&price%3DEUR-max-{max_ppn}-1"
        # distance at the end is meters from (we set to 20km)
        url = f"https://www.booking.com/searchresults.html?latitude={lat}&longitude={lon}&lang=en-us&sb=1&src_elem=sb&src=searchresults&checkin={checkin}&checkout={checkout}&group_adults={adults}&no_rooms={rooms}&group_children=0&selected_currency=EUR&soz=1&lang_changed=1&price%3DEUR-max-{max_ppn}-1&order={order}&nflt=distance%3D20000#map_closed"

        # Scrape hotels based on location
        hotels_data = scrape_hotels(url)
        return Response(hotels_data)



class PostList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    serializer_class = PostSerializer

    filter_backends = [SearchFilter]
    search_fields = ['title', 'text']

    def get_queryset(self):
        festival = self.request.query_params.get('festival')
        filter = self.request.query_params.get('filter')
        sort = self.request.query_params.get('sort')

        if festival:
            queryset =  Post.objects.filter(festival=festival)
        else:
            queryset = Post.objects.all()
        
        if filter:
            if filter == 'Shitpost':
                queryset = queryset.filter(label='shitpost')
            elif filter == 'Lineup':
                queryset = queryset.filter(label='lineup')
            elif filter == 'Travel':
                queryset = queryset.filter(label='travel')
            elif filter == 'Tips':
                queryset = queryset.filter(label='tips')
            else:
                queryset = queryset.all()

        if sort:
            # most likes
            if sort == 'Top':
                queryset = queryset.annotate(top=Count('post_liked_by')).all().order_by('-top')
            elif sort == 'Most commented':
                queryset = queryset.annotate(mc=Count('post_comments')).all().order_by('-mc')
            # best like to dislike ratio
            elif sort == 'Best':
                queryset = queryset.annotate(
                    disliked_by_count=Count('post_disliked_by'),
                    liked_by_count=Count('post_liked_by'),
                ).annotate(
                    ratio=Case(
                        When(disliked_by_count=0, then=F('liked_by_count')),
                        default=F('liked_by_count') / F('disliked_by_count'),
                        output_field=FloatField()
                    )
                ).order_by('-ratio')
            # most dislikes
            elif sort == 'Controversial':
                queryset = queryset.annotate(dislikes=Count('post_disliked_by')).all().order_by('-dislikes')
            else:
                queryset = queryset.order_by('-time')
        return queryset

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
        else:
            instance.edited = True
            
        serializer.save()


# the sorting only works for level 0 comment -> because we use serializer that returns whole structure, but we only want to print from parent
class CommentList(generics.ListCreateAPIView):
    #permission_classes = (IsAuthenticated, )

    serializer_class = CommentSerializer

    def get_queryset(self):
        sort = self.request.query_params.get('sort')
        post = self.kwargs['pk']

        # sorting for top level is here, but for the rest in serializer where we recursively get child_comments
        # (here we only return top level comments as their childs are appended - parent__isnull; without it it would print each comment and then childs)
        if sort == 'Top':
            return Comment.objects.filter(post=post, parent__isnull=True).annotate(top=Count('comment_liked_by')).order_by('-top')
        return Comment.objects.filter(post=post, parent__isnull=True)
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)


def like_or_dislike_comment(instance, user, action):
    if action == 'like':
        instance.comment_disliked_by.remove(user)
        instance.comment_liked_by.add(user) if user not in instance.comment_liked_by.all() else instance.comment_liked_by.remove(user)
    elif action == 'dislike':
        instance.comment_liked_by.remove(user)
        instance.comment_disliked_by.add(user) if user not in instance.comment_disliked_by.all() else instance.comment_disliked_by.remove(user)
    instance.save()

class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes = (IsAuthenticated,)

    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_update(self, serializer):
        instance = serializer.instance
        user = self.request.user
        
        deleted = self.request.data.get('deleted')
        action = self.request.data.get('action')

        if action:
            like_or_dislike_comment(instance, user, action)
        if deleted:
            instance.deleted = deleted

        serializer.save()


        #serializer.save(deleted=deleted)


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

class ChatDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChatSerializer
    
    def get_object(self):
        try:
            return Chat.objects.get(id=self.kwargs['cpk'])
        except Chat.DoesNotExist:
            raise Http404("Chat does not exist")

    def perform_update(self, serializer):
        instance = serializer.instance
        user = self.request.user
        if user not in instance.notified_users.all():
            instance.notified_users.add(user)
        else:
            instance.notified_users.remove(user)
        instance.save()
        serializer.save()


class MessageListPagination(PageNumberPagination):
    page_size = 20

class MessageList(generics.ListCreateAPIView):
    #permission_classes = (IsAuthenticated,)

    serializer_class = MessageSerializer
    pagination_class = MessageListPagination

    # check if chat is in the festival
    def get_queryset(self):
        try:
            chat = Chat.objects.get(id=self.kwargs['cpk'], festival=self.kwargs['pk'])
        except Chat.DoesNotExist:
            raise Http404("Chat does not exist")
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
        data['username'] = user.username
        pusher_client.trigger(f'chat-{message.chat.id}', 'new-message', data)

        ## notifications
        notifications = [
            Notification(user=notified_user, chat=chat, message=message)
            for notified_user in chat.notified_users.all()
            if notified_user != user
        ]
        Notification.objects.bulk_create(notifications)


class NotificationList(generics.ListCreateAPIView):
    serializer_class = NotificationSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user=user, read=False).order_by('-timestamp')