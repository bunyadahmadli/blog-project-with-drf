from django.urls import path 
from .views import CommentCreateAPIView,CommentListAPIView,CommentUpdateAPIView,CommentDeletePIView

app_name ='comments'
urlpatterns = [
    
    path('comments/create/', CommentCreateAPIView.as_view(), name='create'),
    path('comments/', CommentListAPIView.as_view(), name='list'),
    path('comments/update/<pk>', CommentUpdateAPIView.as_view(), name='update'),
    path('comments/delete/<pk>', CommentDeletePIView.as_view(), name='delete'),
]
