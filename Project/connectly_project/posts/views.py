#Validation and Rational Logic | Using Django REST Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment, Like
from .serializers import UserSerializer, PostSerializer, CommentSerializer, LikeSerializer, PostFeedSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

#Restrict Access with RBAC
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsPostAuthor, IsCommentAuthor

#Secure API Endpoints
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .authentication import CsrfExemptSessionAuthentication

#Design Patterns
from .factories.post_factory import PostFactory
from .factories.comment_factory import CommentFactory   #Factory Updated Comments
from .factories.like_factory import LikeFactory

#Update | Delete
from rest_framework import generics


#3rd PT Integration
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
import requests
# from django.conf import settings
from rest_framework.authtoken.models import Token

#Feed/Filter
from django.db.models import Count

#USER
class UserListCreate (APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    # authentication_classes = [CsrfExemptSessionAuthentication]  #Disabled for HTTPS Postman testing
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)

        if user is not None:
            # login(request, user)
            token, created = Token.objects.get_or_create(user=user) #Get or creates token

            return Response({"message": "Authentication successful", "token": token.key})
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#Secure API Endpoints
class ProtectedView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Authenticated"})



#POST
#Factory Pattern | Create Post
class CreatePostView(APIView):  #create using factories
    # authentication_classes = [CsrfExemptSessionAuthentication]  #Disabled for HTTPS Postman testing
    authentication_classes = [TokenAuthentication]

    def post (self, request):
        data = request.data
        user = request.user

        if not user.is_authenticated:
            return Response({"error": "Not authenticated"}, status=401)
        
        author = user

        try:
            post = PostFactory.create_post(
                post_type=data['post_type'],
                title=data['title'],
                content=data.get('content', ''),
                metadata=data.get('metadata', {}),
                author=author
            )
            return Response({'message': 'Post created successfully!', 'post_id': post.id}, 
                            status=status.HTTP_201_CREATED)
        
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
#Post Update | Delete
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = [CsrfExemptSessionAuthentication]  #Disabled for HTTPS Postman testing
    authentication_classes = [TokenAuthentication]

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsPostAuthor]

#Post Get
class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer



#COMMENT
#Get Comments
class CommentListView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    
#Factory Pattern | Create Comments
class CreateCommentView(APIView):
    # authentication_classes = [CsrfExemptSessionAuthentication]  #Disabled for HTTPS Postman testing
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        author = request.user

        try:
            post = Post.objects.get(id=data['post_id'])

            comment = CommentFactory.create_comment(
                                                    post=post,
                                                    author=author,
                                                    text=data['text']
                                                    )

            return Response({"message": "Comment created", "id": comment.id}, status=status.HTTP_201_CREATED)
        
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
#Comment Update | Delete
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes = [CsrfExemptSessionAuthentication]  #Disabled for HTTPS Postman testing
    authentication_classes = [TokenAuthentication]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsCommentAuthor]



#LIKES
#Like Create
class LikePostView(APIView):
    # authentication_classes = [CsrfExemptSessionAuthentication]  #Disabled for HTTPS Postman testing
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


    def post(self, request, post_id):   #Like
        
        user = request.user

        print(request.user)
        print(request.user.is_authenticated)
        
        try:
            post = Post.objects.get(id=post_id)
            like = LikeFactory.create_like(user, post)
            return Response({"message": "Post liked", "likes_count": post.likes.count()}, status=201)
        
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)
        
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
        
    def delete(self, request, post_id): #Unlike | Remove Like
        
        user = request.user
        
        try:
            post = Post.objects.get(id=post_id)
            LikeFactory.remove_like(user, post)
            return Response({"message": "Like removed", "likes_count": post.likes.count()}, status=200)
        
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=404)
        
        except ValueError as e:
            return Response({"error": str(e)}, status=400)


#Like Read
class PostLikesListView(generics.ListAPIView):  #View/List Likes
    serializer_class = LikeSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Like.objects.filter(post_id=post_id)
    

#Feed View
class FeedView(generics.ListAPIView):
    serializer_class = PostFeedSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        queryset = Post.objects.annotate(
            like_count=Count("likes", distinct=True),
            comment_count=Count("comments", distinct=True)
        )

        liked_by = self.request.query_params.get("liked_by")
        if liked_by:
            queryset = queryset.filter(likes__user_id=int(liked_by))
        

        commented_by = self.request.query_params.get("commented_by")
        if commented_by:
            queryset = queryset.filter(comments__author_id=int(commented_by))


        min_like_count = self.request.query_params.get("min_like_count")    #Note: Filter for "Minimum Like Count x"
        if min_like_count:
            queryset = queryset.filter(like_count__gte=int(min_like_count))


        min_comment_count = self.request.query_params.get("min_comment_count")  #Note: Filter for "Minimum Comment Count x"
        if min_comment_count:
            queryset = queryset.filter(comment_count__gte=int(min_comment_count))


        ordering = self.request.query_params.get("ordering")

        if ordering in ["like_count", "-like_count",
                        "comment_count", "-comment_count",
                        "created_at", "-created_at"]:
            queryset = queryset.order_by(ordering)
        else:
            queryset = queryset.order_by("-created_at")

        return queryset
    

#3rd PT Integration
class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "https://127.0.0.1:8000/posts/auth/google/callback/"
