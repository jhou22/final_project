from django.urls import path
from .views import *

urlpatterns = [
    path(r'', home, name='home'),
    path(r'create_comment', CreateCommentView.as_view(), name='create_comment'),
    path(r'random/<int:pk>', RandomPracticePuzzleView.as_view(), name='random_puzzle')
    
]
