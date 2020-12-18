
from django.urls import path
from .views import FavouriteListCreateAPIView,FavouriteAPIView
app_name = 'favourite'
urlpatterns = [
    path('favourites/create', FavouriteListCreateAPIView.as_view(),name='create'),
    path('update-delete/<pk>', FavouriteAPIView.as_view(),name='update-delete')
]
