from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.decorators.cache import never_cache

from . import views

urlpatterns = [
    path('', never_cache(views.PostList.as_view()), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='posts/auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='posts/auth/logout.html'), name='logout'),
    path('profile/', never_cache(views.Profile.as_view()), name='profile'),
    path('create/', views.create_post, name='create')
    # path('profile/', views.profile_view, name='profile')
]