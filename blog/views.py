from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import View, CreateView
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth import login
from django.urls import reverse_lazy


from .models import Post, Tag
from .utils import ObjectDetailMixin, ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin
from .forms import TagForm, PostForm, UserSignUpForm


def main_blog(request):
    return render(request, 'blog/index.html')


class UserSignUp(CreateView):
    form_class = UserSignUpForm
    template_name = 'blog/sign_up.html'
    success_url = reverse_lazy('home_page_url')


class SignUp(View):
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


def log_in_user(request):
    ...


def log_out_user(request):
    logout(request)
    return redirect('home_page_url')


def posts_view(request):
    search_query = request.GET.get('post_search', '')

    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()

    # pagination
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    return render(request, 'blog/posts.html', context={'page': page})


class PostDetail(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class PostCreate(ObjectCreateMixin, View):
    form_model = PostForm
    template = 'blog/post_create.html'


class PostUpdate(ObjectUpdateMixin, View):
    model = Post
    object_form = PostForm
    template = 'blog/post_update.html'


class PostDelete(ObjectDeleteMixin, View):
    model = Post
    delete_template = 'blog/post_delete.html'
    list_template = 'all_posts_url'


def tags_view(request):
    search_query = request.GET.get('tag_search', '')
    if search_query:
        tags = Tag.objects.filter(Q(title__icontains=search_query))
    else:
        tags = Tag.objects.all()
    return render(request, 'blog/tags.html', context={'tags': tags})


class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'


class TagCreate(ObjectCreateMixin, View):
    form_model = TagForm
    template = 'blog/tag_create.html'


class TagUpdate(ObjectUpdateMixin, View):
    model = Tag
    object_form = TagForm
    template = 'blog/tag_update.html'


class TagDelete(ObjectDeleteMixin, View):
    model = Tag
    delete_template = 'blog/tag_delete.html'
    list_template = 'all_tags_url'
