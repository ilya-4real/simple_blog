from django.urls import path
from .views import *

urlpatterns = [
    path('profile_update', ProfileUpdateView.as_view(), name='user_update_url'),
    path('user_profile', ProfileUpdateView.as_view(), name='user_profile_url'),
]