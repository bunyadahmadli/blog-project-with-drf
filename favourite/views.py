from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from .models import Favourite
from .serailizers import FavouriteListCreateSerializer ,FavouriteAPISerializer
from .paginations import FavouritePagination
# Create your views here.

class FavouriteListCreateAPIView(ListCreateAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteListCreateSerializer
    pagination_class =FavouritePagination
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Favourite.objects.filter(user=self.request.user)

    def perform_create(self,serializer):
        serializer.save(user = self.request.user)


class FavouriteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteAPISerializer
    lookup_field ='pk'
    permission_classes = [IsOwner]