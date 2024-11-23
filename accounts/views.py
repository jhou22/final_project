from django.shortcuts import render
from django.views.generic import *
from .forms import *
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

# class CreatePlayerView(CreateView):
#     form_class = CreatePlayerForm
#     template_name = 'accounts/register.html'

class ShowPlayerView(LoginRequiredMixin, DetailView):
    model = PlayerProfile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'
    
class ShowFriendsView(LoginRequiredMixin, ListView):
    model = Friend
    template_name = 'accounts/friends.html'
    context_object_name = 'friends'
    def get_queryset(self):
        pk = self.kwargs['pk']
        user = PlayerProfile.objects.get(pk=pk)
        from_user_friends = super().get_queryset().filter(from_user=user)
        to_user_friends= super().get_queryset().filter(to_user=user)
        return from_user_friends | to_user_friends
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["username"] = PlayerProfile.objects.get(pk=self.kwargs['pk']).username
        return context
        
        
        
    
    
