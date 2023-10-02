from django.shortcuts import render, redirect
from django.views import View
from .forms import UserProfileForm
from .models import UserProfile


class Profile(View):
    def get(self, request, user_id):
        user = UserProfile.objects.get(pk=user_id)
        posts = user.posts.all().select_related('author').prefetch_related('tags')
        context = {'found_user': user,
                   'posts': posts, }

        return render(request, 'blog/profile.html', context=context)

class ProfileUpdateView(View):
    def get(self, request):
        form = UserProfileForm(instance=request.user)
        return render(request, 'accounts/user_update.html', context={'form': form})

    def post(self, request):
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home_page_url')
        else:
            return render(request, 'accounts/user_update.html', context={'form': form})
