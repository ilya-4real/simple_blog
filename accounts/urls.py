from django.urls import path
from django.conf.urls.static import static

from web import settings
from .views import *

urlpatterns = [
    path('profile_update/', ProfileUpdateView.as_view(), name='user_update_url'),
    path('<int:user_id>/', UserProfile1.as_view(), name='user_profile_url'),
    path('log_out/', log_out_user, name='log_out_url'),
    path('log_in/', UserLogIn.as_view(), name='log_in_url'),
    path('sign_up/', SignUp.as_view(), name='sign_up_url')
]
