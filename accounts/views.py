from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.contrib.auth import logout
from django.views.generic import *
from .forms import *
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class ShowPlayerView(LoginRequiredMixin, DetailView):
    '''Shows a player and passes in potential friend relationships if it exists'''
    model = PlayerProfile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        from_user = PlayerProfile.objects.get(user=self.request.user)
        to_user = PlayerProfile.objects.get(pk=self.kwargs['pk'])
        if from_user == to_user:
            context["is_friends"] = "Is itself"
        else:
            if from_user.is_friends(to_user):
                context['is_friends'] = True
                context['friends_since'] = from_user.friends_since(to_user)
            else:
                context['is_friends'] = False
        return context
    
    
class ShowFriendsView(LoginRequiredMixin, ListView):
    '''shows all friends based on user'''
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

# https://stackoverflow.com/questions/38047408/how-to-allow-user-to-delete-account-in-django-allauth
class DeletePlayerView(LoginRequiredMixin, DeleteView):
    '''deletes an account'''
    model = User
    success_url = reverse_lazy('home')
    template_name = 'accounts/delete_profile.html'
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context["form"] = DeletePlayerForm()
        return context
    
    
    def get_object(self, queryset = ...):
        return self.request.user
    
    def delete(self, request, *args, **kwargs):
        form = DeletePlayerForm(request.POST)
        if form.is_valid():
            user = request.user
            # Logout before we delete. This will make request.user
            # unavailable (or actually, it points to AnonymousUser).
            logout(request)
            # Delete user (and any associated ForeignKeys, according to
            # on_delete parameters).
            user.delete()
        return
    
    # def get(self, request, *args, **kwargs):
    #     form = DeletePlayerForm()
    #     return render(request, 'accounts/delete_profile.html', {'form': form})
    
    # def post(self, request, *args, **kwargs):
    #     form = DeletePlayerForm(request.POST)
    #     # Form will be valid if checkbox is checked.
    #     if form.is_valid():
    #         user = request.user
    #         # Logout before we delete. This will make request.user
    #         # unavailable (or actually, it points to AnonymousUser).
    #         logout(request)
    #         # Delete user (and any associated ForeignKeys, according to
    #         # on_delete parameters).
    #         user.delete()
    #         return redirect(reverse('home'))
    #     return render(request, 'accounts/delete_profile.html', {'form': form})
    
class UpdatePlayerView(LoginRequiredMixin, UpdateView):
    '''updates a player's information'''
    form_class = UpdatePlayerForm
    model = PlayerProfile
    template_name = 'accounts/update_profile.html'
    
    def get_object(self, queryset = ...):
        return PlayerProfile.objects.get(user=self.request.user)
    def form_valid(self, form):
        email = form.instance.email
        username = form.instance.username
        print(f'UpdateProfileView: form.cleaned_data={form.cleaned_data}')
        User.objects.filter(pk=form.instance.pk).update(email=email)
        User.objects.filter(pk=form.instance.pk).update(username=username)
        return super().form_valid(form)

class ProfileListView(LoginRequiredMixin, ListView):
    '''shows all profiles based on search queries'''
    template_name = 'accounts/profiles.html'
    context_object_name = 'profiles'
    model = PlayerProfile
    paginate_by = 100
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = SearchPlayersForm()
        return context
    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.method == 'GET':
            form = SearchPlayersForm(self.request.GET)
            if form.is_valid():
                name = form.cleaned_data['username']
                print('username is')
                print(name)
                print('before')
                print(qs)
                qs = qs.filter(username__icontains=name)
                print("after")
                print(qs)
        return qs

class CreateFriendView(LoginRequiredMixin, View):
    '''creates friend'''
    def dispatch(self, request, *args, **kwargs):
        from_user = PlayerProfile.objects.get(user=self.request.user)
        to_user = PlayerProfile.objects.get(pk=kwargs.get('to_user_pk'))
        from_user.add_friend(to_user)
        return redirect(reverse('profile', kwargs={'pk':kwargs.get('to_user_pk')}))
    
    