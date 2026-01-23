# from django.shortcuts import render

# Create your views here.
# import json

# from django.http import JsonResponse
# from .models import User
# from .models import Post
# from django.views.decorators.csrf import csrf_exempt

#         #Retrieve all users (GET)
# def get_users(request):

#     try:
#         users = list (User.objects.values('id', 'username','email','created_at'))
#         return JsonResponse (users, safe = False)
#     except Exception as e:
#         return JsonResponse ({'error': str(e)}, status = 500)


#         #Create a user (POST)
# # import json
# # from django.http import JsonResponse
# # from django.views.decorators.csrf import csrf_exempt
# # from .models import User

# @csrf_exempt
# def create_user(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             user = User.objects.create(username=data['username'], email = data['email'])
#             return JsonResponse({'id': user.id, 'message': 'User created successfully'}, status = 201)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status = 400)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status = 405)


#         #Update a User (Update)
# @csrf_exempt
# def update_user(request, id):
#     if request.method == 'PUT':
#         try:
#             data = json.loads(request.body)
#             user = User.objects.get(id=id)

#             user.username = data.get('username', user.username)
#             user.email = data.get('email', user.email)
#             user.save()

#             return JsonResponse({'message': 'User updated successfully'})
#         except User.DoesNotExist:
#             return JsonResponse({'error': 'User not found'}, status=404)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)


#         #Delete a User (Delete)
# @csrf_exempt
# def delete_user(request, id):
#     if request.method == 'DELETE':
#         try:
#             user = User.objects.get(id=id)
#             user.delete()
#             return JsonResponse({'message': 'User deleted successfully'})
#         except User.DoesNotExist:
#             return JsonResponse({'error': 'User not found'}, status=404)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)


#         #Retrieve all Posts (GET)
# # from .models import Post
# def get_posts(request):
#     try:
#         posts = list(Post.objects.values('id','content','author','created_at'))
#         return JsonResponse(posts, safe = False)
#     except Exception as e:
#         return JsonResponse({'error', str(e)}, status = 500)


#         #Create a Post (POST)
# @csrf_exempt
# def create_post(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             author = User.objects.get(id = data['author'])
#             post = Post.objects.create(content = data['content'], author = author)
#             return JsonResponse({'id': post.id, 'message': 'Post created successfully'}, status = 201)
#         except User.DoesNotExist:
#             return JsonResponse({'error':'Author not found'}, status = 404)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status = 400)
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status = 405)
    
#UPDATED VERSION
#Validation and Rational Logic | Using Django REST Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Post, Comment
from .serializers import UserSerializer, PostSerializer, CommentSerializer


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
    
