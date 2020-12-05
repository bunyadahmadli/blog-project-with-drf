from rest_framework.generics import CreateAPIView, ListAPIView,UpdateAPIView,DestroyAPIView
from .models import Comment
from .serializers import CommentCreateSerializer, CommentListSerializer, CommentUpdateDeleteSerializer
from .permissions import IsOwner
# Create your views here.
class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def perform_create(self,serializer):
        serializer.save(user =self.request.user)

class CommentListAPIView(ListAPIView):
    queryset =Comment.objects.all()
    serializer_class = CommentListSerializer
    def get_queryset(self):
        return Comment.objects.filter(parent=None)


class CommentUpdateAPIView(UpdateAPIView):
    queryset=Comment.objects.all()
    serializer_class = CommentUpdateDeleteSerializer

class CommentDeletePIView(DestroyAPIView):
    queryset=Comment.objects.all()
    serializer_class = CommentUpdateDeleteSerializer
    lookup_field= 'pk'
    permission_classes = [IsOwner]