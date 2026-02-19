from django.db import models
from django.contrib.auth.models import User
# Create your models here.
    

class Post (models.Model):
    Text = "text"
    Image = "image"
    Video = "video"

    POST_TYPES =[('text', "Text"), ('image', "Image"), ('video', "Video"),]


    content = models.TextField()    #The text content of the post
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)  #the user who created the post
    created_at = models.DateTimeField(auto_now_add=True)    #Timestamp when the post was created

    #Factory Pattern update
    post_type = models.CharField(max_length=10, choices=POST_TYPES, default=Text)
    metadata = models.JSONField(default=dict, blank=True)
    title = models.CharField(max_length=200, default="Untitled")

    def __str__(self):
        return f"Post by {self.author.username} at {self.created_at}"
    

class Comment (models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return f"Comment by {self.author.username} on Post {self.post.id}"
    

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: #prevent duplicate likes
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} likes Post {self.post.id}"



