from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('practise/', views.practise, name='practise'),
    path('manage_packs/', views.manage_packs, name='manage_packs'),
    path('manage_flashcards/<int:pack_id>/',
         views.manage_flashcards, name='manage_flashcards'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('password_reset/', views.password_reset, name='password_reset'),
    path('create_pack/', views.create_pack, name='create_pack'),
    path('create_flashcard/<int:pack_id>',
         views.create_flashcard, name='create_flashcard'),
    path('edit_flashcard/<int:flashcard_id>',
         views.edit_flashcard, name='edit_flashcard'),
    path('delete_flashcard/<int:flashcard_id>',
         views.delete_flashcard, name='delete_flashcard'),
    path('review/<int:pack_id>', views.review, name='review'),
    path('delete_pack/<int:pack_id>',
         views.delete_pack, name='delete_pack'),
    path('edit_pack/<int:pack_id>', views.edit_pack, name='edit_pack'),
]
