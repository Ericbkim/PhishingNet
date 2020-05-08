from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='phish-home'),
    path('assigned/', views.assigned, name='phish-assigned'),
    path('created/', views.created, name='phish-created'),
    path('logout/', auth_views.LogoutView.as_view(template_name='home/logout.html', next_page='phish-login'), name='phish-logout'),
    path('login/', auth_views.LoginView.as_view(template_name='home/login.html', redirect_field_name='phish-home'), name='phish-login'),
    path('edit/', views.edit, name='phish-edit'),
    path('upload/', views.upload, name='phish-upload'),
    path('register/', views.register, name='phish-register'),
    path('suggested/', views.suggested, name='phish-suggested'),
    path('post/<int:postId>/', views.post, name='phish-post'),
    path('email/', views.email, name='phish-email'), # For testing purposes
]