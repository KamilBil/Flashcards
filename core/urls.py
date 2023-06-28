from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('practice/', views.practice, name='practice'),
    path('manage/', views.manage, name='manage'),
    path('dashboard/', views.dashboard, name='dashboard'),
]