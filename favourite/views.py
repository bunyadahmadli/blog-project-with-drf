from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .models import Favourite
from .serailizers import FavouriteListCreateSerializer
# Create your views here.

class FavouriteListCreateAPIView(ListCreateAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteListCreateSerializer

    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)

    def perform_create(self,serializer):
        serializer.save(user = self.request.user)

    def validate(self, attrs):
        print(attrs["post"])
        print(attrs["user"])

        return attrs