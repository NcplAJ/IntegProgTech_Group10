# from django.shortcuts import render

# Create your views here.
# import json


#Validation and Rational Logic | Using Django REST Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Post, Comment
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


        # username = request.data.get("username")
        # password = request.data.get("password")
        # email = request.data.get("email")

        # if not username or not password:
        #     return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # #built in Django create_user
        # user = User.objects.create_user(username=username, password=password, email=email)

        # return Response({"id":user.id, "username":user.username, "email":user.email, "message":"User created successfully"}, status=status.HTTP_201_CREATED)

class PostListCreate(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
    

class LoginView(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
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
        

class PostDetailView(APIView):
    permission_classes = [IsAuthenticated, IsPostAuthor]

    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        self.check_object_permissions(request, post)
        return Response({"content": post.content})
    

#Secure API Endpoints
class ProtectedView(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Authenticated"})