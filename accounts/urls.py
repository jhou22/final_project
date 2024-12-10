from django.urls import path
from .views import *
urlpatterns = [
    path(r'<int:pk>', ShowPlayerView.as_view(), name="profile"),
    path(r'profiles', ProfileListView.as_view(), name="profiles"),
    path(r'update', UpdatePlayerView.as_view(), name="update_profile"),
    path(r'delete', DeletePlayerView.as_view(), name="delete_profile"),
    path(r'<int:pk>/friends', ShowFriendsView.as_view(), name="friends"),
    path(r'add_friend/<int:to_user_pk>', CreateFriendView.as_view(), name='add_friend'),
]
