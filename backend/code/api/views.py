from django.http import JsonResponse
from .choices import COUNTRIES

from api.models import Festival, Post
from api.serializers import FestivalSerializer, PostSerializer

from rest_framework import generics, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# Create your views here.
def countries(request):
    return JsonResponse(dict(COUNTRIES))


class FestivalList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer

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

    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_update(self, serializer):
        instance = serializer.instance
        user = self.request.user
        action = self.request.data.get('action')

        if action:
            like_or_dislike(instance, user, action)
            
        serializer.save()