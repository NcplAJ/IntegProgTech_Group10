from django.db import models

# Create your models here.

class User (models.Model):  #Models = column in a table / database
    username = models.CharField(max_length = 100, unique = True)    #User's unique name
    email = models.EmailField(unique = True)    #User's unique email
    created_at = models.DateTimeField(auto_now_add = True)  #Timestamp when the user was created

    def __str__(self):  #special method to control returned when converting an object to a string
        return self.username
    

class Post(models.Model):
    content = models.TextField()    #The text conent of the post
    author = models.ForeignKey(User, on_delete=models.CASCADE)  #the user who created the post
    created_at = models.DateTimeField(auto_now_add=True)    #Timestamp when the post was created

    def __str__(self):
        return self.content[:50]