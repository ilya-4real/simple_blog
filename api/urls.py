from django.urls import path, include
from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'tags', TagViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # path('posts/', PostViewSet.as_view({'get': 'list'})),
    # path('posts/<int:pk>', PostViewSet.as_view({'put': 'update'})),
    # path('posts/<int:pk>', PostViewSet.as_view({'get': 'retrieve'})),
    # path('tags/', TagsApiView.as_view(), name='tags.url'),
]
