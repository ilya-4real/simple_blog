from django.contrib.auth import logout, login, authenticate
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserProfileForm, UserLogInForm, UserSignUpForm
from .models import UserProfile
from django.urls import reverse
from .tasks import print_something_terminal


class UserProfile1(View):
    def get(self, request, user_id):
        user = UserProfile.objects.filter(pk=user_id)[0]
        posts = user.posts.all().select_related('author').prefetch_related('tags')
        is_owner = user == request.user
        context = {'found_user': user,
                   'posts': posts,
                   'is_owner': is_owner}

        return render(request, 'accounts/profile.html', context=context)


class ProfileUpdateView(View):
    def get(self, request):
        form = UserProfileForm(instance=request.user)
        return render(request, 'accounts/user_update.html', context={'form': form})

    def post(self, request):
        print(request.POST)
        print(request.FILES)
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            return redirect(reverse('user_profile_url', args=[request.user.id]))
        else:
            return render(request, 'accounts/user_update.html', context={'form': form})


def log_out_user(request):
    logout(request)
    # print_something_terminal.delay('everything is good')
    return redirect('home_page_url')


class SignUp(View):
    """this is my implementation"""

    def get(self, request):
        bound_form = UserSignUpForm()
        return render(request, 'accounts/sign_up.html', context={'form': bound_form})

    def post(self, request):
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_update_url')
        else:
            return render(request, 'accounts/sign_up.html', context={'form': form})


class UserLogIn(View):
    def get(self, request):
        form = UserLogInForm()
        return render(request, 'accounts/log_in.html', context={'form': form})

    def post(self, request):
        form = UserLogInForm()
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_page_url')
        else:
            return render(request, 'accounts/log_in.html', context={'form': form})
