from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views.generic import View, CreateView
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Tag
from .utils import ObjectDetailMixin, ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin
from .forms import TagForm, PostForm, UserSignUpForm, UserLogInForm


def main_blog(request):
    return render(request, 'blog/index.html')


class UserSignUp(CreateView):
    """this is a built-in implementation of user sign-up view"""
    form_class = UserSignUpForm
    template_name = 'blog/sign_up.html'
    success_url = reverse_lazy('home_page_url')


class SignUp(View):
    """this is my implementation"""

    def get(self, request):
        bound_form = UserSignUpForm()
        return render(request, 'blog/sign_up.html', context={'form': bound_form})

    def post(self, request):
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home_page_url')
        else:
            return render(request, 'blog/sign_up.html', context={'form': form})


class UserLogIn(View):
    def get(self, request):
        form = UserLogInForm()
        return render(request, 'blog/log_in.html', context={'form': form})

    def post(self, request):
        form = AuthenticationForm()
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_page_url')
        else:
            return render(request, 'blog/log_in.html', context={'form': form})


def log_out_user(request):
    logout(request)
    return redirect('home_page_url')


class UserProfile(View):
    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        posts = user.posts.all().prefetch_related('tags')
        if request.user == user and posts.count():
            profile_description = 'Your posts:'
        elif request.user != user and posts.count():
            profile_description = 'Posts written by this user:'
        else:
            profile_description = 'There are no posts here yet...'
        return render(request, 'blog/profile.html', context={'user': user, 'posts': posts, 'profile_description': profile_description})


def posts_view(request):
    search_query = request.GET.get('post_search', '')

    # searching engine try elastic FIXME
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query)).select_related('author')
    else:
        posts = Post.objects.all().select_related('author').prefetch_related('tags')

    # pagination FIXME
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    return render(request, 'blog/posts.html', context={'page': page})


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = PostForm
    template = 'blog/post_create.html'
    login_url = 'log_in_url'


class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    object_form = PostForm
    template = 'blog/post_update.html'
    login_url = 'log_in_url'


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    delete_template = 'blog/post_delete.html'
    list_template = 'all_posts_url'
    login_url = 'log_in_url'


def tags_view(request):
    # same: try elastic or something else FIXME
    search_query = request.GET.get('tag_search', '')
    if search_query:
        tags = Tag.objects.filter(Q(title__icontains=search_query))
    else:
        tags = Tag.objects.all()
    return render(request, 'blog/tags.html', context={'tags': tags})


class TagDetail(View):
    def get(self, request, slug):
        tag = Tag.objects.get(slug__iexact=slug)
        posts = tag.posts.all().select_related('author').prefetch_related('tags')
        return render(request, 'blog/tag_detail.html', context={'tag': tag, 'posts': posts})


class TagCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = TagForm
    template = 'blog/tag_create.html'
    login_url = 'log_in_url'


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    object_form = TagForm
    template = 'blog/tag_update.html'
    login_url = 'log_in_url'


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    delete_template = 'blog/tag_delete.html'
    list_template = 'all_tags_url'
    login_url = 'log_in_url'
