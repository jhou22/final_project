from django.urls import path
from .views import *

urlpatterns = [
    path(r'', home, name='home'),
    path(r'create_comment', CreateCommentView.as_view(), name='create_comment')
]
