from django.urls import path
from .views import *

from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', main_blog, name='home_page_url'),
    path('post/', posts_view, name='all_posts_url'),
    path('post/create/', PostCreate.as_view(), name='post_create_url'),
    path('post/<str:slug>/', PostDetail.as_view(), name='post_detail_url'),
    path('post/<str:slug>/update/', PostUpdate.as_view(), name='post_update_url'),
    path('post/<str:slug>/delete/', PostDelete.as_view(), name='post_delete_url'),
    path('tag/', tags_view, name='all_tags_url'),
    path('tag/create/', TagCreate.as_view(), name='tag_create_url'),
    path('tag/<str:slug>', TagDetail.as_view(), name='tag_detail_url'),
    path('tag/<str:slug>/update/', TagUpdate.as_view(), name='tag_update_url'),
    path('tag/<str:slug>/delete/', TagDelete.as_view(), name='tag_delete_url'),
    path('newsfeed/', cache_page(60*5)(NewsFeed.as_view()), name='news_feed_url'),
]
