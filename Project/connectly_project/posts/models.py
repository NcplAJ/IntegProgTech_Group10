from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
    
#New RBACpy
class User(AbstractUser):
    class UserRole(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        USER = "USER", "User"
        GUEST = "GUEST", "Guest"
    
    role = models.CharField(max_length=10, choices=UserRole.choices, default=UserRole.GUEST)

    groups = models.ManyToManyField('auth.Group', related_name='posts_user_set', blank=True,
                                    help_text='The groups this user belongs to.', verbose_name='groups',)

    user_permissions = models.ManyToManyField('auth.Permission', related_name='posts_user_permissions_set', blank=True,
                                                help_text='Specific permissions for this user.', verbose_name='user permissions',)

#New Privacy
class PrivacyLevel(models.TextChoices):
    PUBLIC = "PUBLIC", "Public"
    PRIVATE = "PRIVATE", "Private"


class Post (models.Model):
    Text = "text"
    Image = "image"
    Video = "video"

    POST_TYPES =[('text', "Text"), ('image', "Image"), ('video', "Video"),]
    #New
    privacy = models.CharField(
        max_length=10,
        choices=PrivacyLevel.choices,
        default=PrivacyLevel.PUBLIC
    )


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



