from rest_framework.generics import CreateAPIView, ListAPIView,UpdateAPIView,DestroyAPIView,RetrieveUpdateAPIView
from rest_framework.mixins import UpdateModelMixin,DestroyModelMixin
from .models import Comment
from .serializers import CommentCreateSerializer, CommentListSerializer, CommentUpdateDeleteSerializer
from .permissions import IsOwner
from .paginations import CommentPagination
# Create your views here.
class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def perform_create(self,serializer):
        serializer.save(user =self.request.user)

class CommentListAPIView(ListAPIView):
    serializer_class = CommentListSerializer
    pagination_class = CommentPagination
    def get_queryset(self):
        queryset=Comment.objects.filter(parent=None)
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(post=query )
        return queryset


class CommentUpdateAPIView(DestroyModelMixin,UpdateAPIView,RetrieveUpdateAPIView):
    queryset=Comment.objects.all()
    serializer_class = CommentUpdateDeleteSerializer
    lookup_field= 'pk'
    permission_classes = [IsOwner]

    def delete(self, request, *args, **kwargs):
        return self.destroy(request,*args,**kwargs)

class CommentDeletePIView(DestroyAPIView):
    queryset=Comment.objects.all()
    serializer_class = CommentUpdateDeleteSerializer
    lookup_field= 'pk'
    permission_classes = [IsOwner]