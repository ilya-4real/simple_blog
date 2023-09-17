from django.urls import path
from .views import PostsApiView

urlpatterns = [
    path('', PostsApiView.as_view(), name='test_url')
]