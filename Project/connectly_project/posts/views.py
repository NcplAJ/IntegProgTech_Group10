# from django.shortcuts import render

# Create your views here.
# import json

#Validation and Rational Logic | Using Django REST Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

#Restrict Access with RBAC
from rest_framework.permissions import IsAuthenticated
from .permissions import IsPostAuthor

#Secure API Endpoints
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .authentication import CsrfExemptSessionAuthentication

#Design Patters
from .factories.post_factory import PostFactory

#Update | Delete
from rest_framework import generics


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
    authentication_classes = [CsrfExemptSessionAuthentication]  #For HTTPS Postman testing
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({"message": "Authentication successful"})
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#Secure API Endpoints
class ProtectedView(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Authenticated"})



#COMMENT
class CommentListCreate(APIView):
    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    
#POST
#Factory Pattern | Create
class CreatePostView(APIView):  #create using factories
    authentication_classes = [CsrfExemptSessionAuthentication]  #For HTTPS Postman testing

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
    authentication_classes = [CsrfExemptSessionAuthentication]  #For HTTPS Postman testing
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsPostAuthor]

#Post Get
class PostListCreate(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer