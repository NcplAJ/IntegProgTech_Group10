from django.urls import path
# from . import views
from .views import UserListCreate, PostListCreate, CommentListCreate, LoginView, ProtectedView, CreatePostView

urlpatterns = [
    #User (OLD)
    # path('users/', views.get_users, name = 'get_users'),
    # path('users/create/', views.create_user, name = 'create_user'),
    # path('user/update/<int:id>/', views.update_user),
    # path('user/delete/<int:id>/', views.delete_user),

    # #Posts
    # path('posts/', views.get_posts, name = 'get_posts'),
    # path('posts/create/', views.create_post, name = 'create_post'),

    #DRF Ver
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('posts/', PostListCreate.as_view(), name='post-list-create'),
    path('comments/', CommentListCreate.as_view(), name='comment-list-create'),
    path('login/', LoginView.as_view(), name='login'),
    path("protected/", ProtectedView.as_view(), name="protected"),
    path("create/", CreatePostView.as_view(), name="factory-create-post"),

]
