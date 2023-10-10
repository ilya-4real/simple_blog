from django.shortcuts import render, redirect
from django.views.generic import View
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.modules.services import paginate
from django.urls import reverse

from .models import Post, Tag
from .modules.scrapper import Scraper
from .utils import ObjectDetailMixin, ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin
from .forms import TagForm, PostForm, CommentForm


def main_blog(request):
    return render(request, 'blog/index.html')


def posts_view(request):
    search_query = request.GET.get('post_search', '')

    if search_query:
        posts = (
            Post.objects
            .filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
            .select_related('author')
            .prefetch_related('tags')
        )
    else:
        posts = (
            Post.objects
            .all()
            .select_related('author')
            .prefetch_related('tags')
        )

    page = paginate(request.GET.get('page'), posts, 5)
    return render(request, 'blog/posts.html', context={'page': page})


class PostDetail(View):
    def get(self, request, slug):
        post = Post.objects.filter(slug=slug).select_related('author')[0]
        comment_form = CommentForm()
        comments = post.comment.all().select_related('author').values('author__username', 'body', 'pub_date')
        context = {'post': post,
                   'comments': comments,
                   'comment_form': comment_form}
        return render(request, 'blog/post_detail.html', context=context)

    def post(self, request, slug):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = Post.objects.get(slug=slug)
            comment.save()
            form.save_m2m()
            return redirect(reverse('post_detail_url', args=[slug]))
        else:
            return redirect('home_page_url')


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
    search_query = request.GET.get('tag_search', '')
    if search_query:
        tags = Tag.objects.filter(Q(title__icontains=search_query))
    else:
        tags = Tag.objects.all()
    return render(request, 'blog/tags.html', context={'tags': tags})


class TagDetail(View):
    def get(self, request, slug):
        tag = Tag.objects.get(slug__iexact=slug)
        posts = (
            tag
            .posts
            .all()
            .select_related('author')
            .prefetch_related('tags')
        )
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


class NewsFeed(View):
    login_url = 'log_in_url'

    def get(self, request):
        scrapped = Scraper('https://news.yahoo.com/rss')
        channel = scrapped.scrap_channel()
        items = scrapped.scrap_item(10)

        context = {
            'channel': channel,
            'items': items,
        }

        return render(request, 'blog/newsfeed.html', context)
