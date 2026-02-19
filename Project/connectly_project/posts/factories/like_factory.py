from posts.models import Like

class LikeFactory:
    @staticmethod
    def create_like(user, post):
        like, created = Like.objects.get_or_create(user=user, post=post)

        if not created:
            raise ValueError("User has already liked this post")
        
        return like
    
    @staticmethod
    def remove_like(user,post):
        try:
            like = Like.objects.get(user=user, post=post)
            like.delete()
            return True
        
        except Like.DoesNotExist:
            raise ValueError("Like does not exist")