from django.urls import path
from .views import *

from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', main_blog, name='home_page_url'),
    path('profile/<int:user_id>', UserProfile.as_view(), name='user_profile_url'),
    path('log_in/', UserLogIn.as_view(), name='log_in_url'),
    path('sign_up/', SignUp.as_view(), name='sign_up_url'),
    path('log_out', log_out_user, name='log_out_url'),
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
