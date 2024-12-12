from django.urls import path
from .views import *

urlpatterns = [
    path(r'', home, name='home'), # home view
    path(r'create_comment', CreateCommentView.as_view(), name='create_comment'), # comment creation
    path(r'random/<int:pk>', RandomPracticePuzzleView.as_view(), name='random_puzzle') # random puzzle
    
]
