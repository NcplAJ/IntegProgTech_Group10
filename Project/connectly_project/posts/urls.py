from django.urls import path
from . import views

urlpatterns = [
    #User
    path('users/', views.get_users, name = 'get_users'),
    path('users/create/', views.create_user, name = 'create_user'),
    path('user/update/<int:id>/', views.update_user),
    path('user/delete/<int:id>/', views.delete_user),

    #Posts
    path('posts/', views.get_posts, name = 'get_posts'),
    path('posts/create/', views.create_post, name = 'create_post'),
]
