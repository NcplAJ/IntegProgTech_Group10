from ..models import Comment, Post

class CommentFactory:
    @staticmethod
    def create_comment(post, author, text):
        """
        post: Post instance
        author: User instance
        text: string
        """
        if not post or not author:
            raise ValueError("Post and author are required")
        
        comment = Comment.objects.create(post=post, author=author, text=text)

        return comment