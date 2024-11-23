from django.urls import path
from .views import *
urlpatterns = [
    path(r'<int:pk>', ShowPlayerView.as_view(), name="profile"),
    path(r'<int:pk>/friends', ShowFriendsView.as_view(), name="friends")
]
