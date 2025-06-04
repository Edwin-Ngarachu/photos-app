from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('photo/<int:pk>/', views.photo_detail, name='photo_detail'),
    path('photo/<int:pk>/like/', views.like_photo, name='like_photo'),
    path('upload/', views.upload_photo, name='upload_photo'),
    path('profile/<str:username>/', views.profile, name='profile'),
    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(
        template_name='photo_gallery/login.html',
        extra_context={'title': 'Login'}
    ), name='login'),
    
    path('logout/', auth_views.LogoutView.as_view(
        template_name='photo_gallery/logout.html',
        next_page='home'  # Add this to specify where to redirect after logout
    ), name='logout'),
    
    path('register/', views.register, name='register'),
]