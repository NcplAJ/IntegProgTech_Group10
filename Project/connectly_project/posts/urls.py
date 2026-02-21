from django.urls import path, include
from .views import (UserListCreate, LoginView, ProtectedView, 
                    CreatePostView, PostDetailView, PostListCreate, 
                    CommentListView,  CreateCommentView, CommentDetailView, 
                    LikePostView, PostLikesListView,
                    GoogleLogin)


urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    
    
    path('login/', LoginView.as_view(), name='login'),
    path("protected/", ProtectedView.as_view(), name="protected"),
    
    # path('posts/', PostListCreate.as_view(), name='post-list-create'),    #Serializer Create
    path('create/', CreatePostView.as_view(), name="factory-create-post"),  #Factory Create
    path('<int:pk>/', PostDetailView.as_view(), name="post-detail"),  #Post Update | Delete
    path('', PostListCreate.as_view(), name='post-list'), #Get current Posts    -url = /posts/

    #Comment
    path('comments/', CommentListView.as_view(), name='comment-list'),  #Get Comments
    path('comments/create/', CreateCommentView.as_view(), name='comment-create'),   #Post Comments
    path('comments/<int:pk>/', CommentDetailView.as_view(), name="comment-detail"),  #Comment Update | Delete

    #Likes
    path('<int:post_id>/like/', PostLikesListView.as_view(), name='post-likes'),   
    path('<int:post_id>/likes/', LikePostView.as_view(), name="like-post"), #Like and Unlike

    #3rd PT Integration
    path('auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('accounts/', include('allauth.urls')),
    path('auth/user/', include('dj_rest_auth.urls')), #User profile | Note: use 'auth/user/user/
]
