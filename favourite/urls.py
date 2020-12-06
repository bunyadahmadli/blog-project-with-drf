
from django.urls import path
from .views import FavouriteListCreateAPIView
app_name = 'favourite'
urlpatterns = [
    path('favourites/create', FavouriteListCreateAPIView.as_view(),name='favourite')
]
