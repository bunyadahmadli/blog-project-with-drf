from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='post:detail',
        lookup_field='slug'
    )

    username = serializers.SerializerMethodField() 
    class Meta:
        model =Post
        fields =[
            'username',
            'title', 
            'content',
            'image',
            'url',
            'created',
            'modified_by'
        ]
    def get_username(self,obj):
        return obj.user.username

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