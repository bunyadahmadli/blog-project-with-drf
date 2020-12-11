
from rest_framework import serializers
from .models import Favourite

class FavouriteListCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields='__all__'

    def validate(self, attrs):
        queryset =Favourite.objects.filter(post = attrs["post"],user =attrs["user"])
        if queryset.exists():
            raise serializers.ValidationError("Zaten favorilere eklendi")
        return attrs