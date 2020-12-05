from django.shortcuts import render
from rest_framework.generics import ListAPIView , RetrieveAPIView, DestroyAPIView, UpdateAPIView,CreateAPIView,RetrieveUpdateAPIView
from post.models import Post
from .serializers import PostSerializer,PostCreateUpdateSerializer
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from .permissions import IsOwner
from rest_framework.filters import SearchFilter

class PostListAPIView(ListAPIView):
    serializer_class = PostSerializer
    filter_backends =[SearchFilter]
    search_fields =['title']

    def get_queryset(self):
        queryset = Post.objects.filter(draft =False)
        return queryset
    

class PostDetailAPIView(RetrieveAPIView):
    queryset= Post.objects.all()
    serializer_class =PostSerializer
    lookup_field = 'slug'

class PostDeleteAPIView(DestroyAPIView):
    queryset= Post.objects.all()
    serializer_class =PostSerializer
    lookup_field = 'slug'
    permission_classes =[IsOwner]

class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset= Post.objects.all()
    serializer_class =PostCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes =[IsOwner]
    def perform_update(self,serializer):
        serializer.save(modified_by =self.request.user)

class PostCreateAPIView(CreateAPIView):
    queryset= Post.objects.all()
    serializer_class =PostCreateUpdateSerializer
    permission_classes = [IsOwner]

    def perform_create(self,serializer):
        serializer.save(user =self.request.user)