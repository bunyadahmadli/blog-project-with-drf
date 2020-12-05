from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='post:detail',
        lookup_field='slug'
    )
    class Meta:
        model =Post
        fields =[
            'user',
            'title', 
            'content',
            'image',
            'url',
            'created',
            'modified_by'
        ]


class PostCreateUpdateSerializer(serializers.ModelSerializer):
   
    class Meta:
        model =Post
        fields =[
            'title',
            'content',
            'image',
        ]
    def save(self,**kwargs):
        return True