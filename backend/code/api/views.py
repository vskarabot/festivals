from django.http import JsonResponse
from .choices import COUNTRIES

from api.models import Festival
from api.serializers import FestivalSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

# Create your views here.
def countries(request):
    return JsonResponse(dict(COUNTRIES))


class FestivalList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer

    # add the user that sent request (when creating new) to festival mods
    def perform_create(self, serializer):
        festival = serializer.save()
        festival.mods.add(self.request.user)


class FestivalDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = Festival.objects.all()
    serializer_class = FestivalSerializer