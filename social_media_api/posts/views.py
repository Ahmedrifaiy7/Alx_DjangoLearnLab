from rest_framework import viewsets, permissions, status
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import  Like
from notifications.models import Notification
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        post = self.get_object()
        if post.author != self.request.user:
            raise permissions.PermissionDenied("You do not have permission to edit this post.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise permissions.PermissionDenied("You do not have permission to delete this post.")
        instance.delete()

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise permissions.PermissionDenied("You do not have permission to edit this comment.")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise permissions.PermissionDenied("You do not have permission to delete this comment.")
        instance.delete()

class FeedView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.request.user
        # Filter posts from users the current user follows
        followed_users = user.following.all()
        return self.queryset.filter(author__in=followed_users).order_by('-created_at')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_post(request, pk):
  post = get_object_or_404(Post, pk=pk)  # Correct use of get_object_or_404 to get the post by primary key
    # Create or get the Like object for the current user and post
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if created:
        return Response({"detail": "Post liked successfully."}, status=201)  # Liked the post
    else:
        return Response({"detail": "You have already liked this post."}, status=200)  # Already liked the post

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def unlike_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        user = request.user
        like = Like.objects.filter(user=user, post=post)
        if like.exists():
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT) #Return 204 on successful delete
        else:
            return Response({"error": "You haven't liked this post"}, status=status.HTTP_400_BAD_REQUEST)
    except Post.DoesNotExist:
        return Response({"error": "Post does not exist"}, status=status.HTTP_404_NOT_FOUND)

def get(request):
    """
    View to get the feed of posts from users the current user is following.
    """
    # Get the users the current user is following
    followed_users = request.user.following.all()

    # Fetch posts from these users, ordered by creation date (most recent first)
    posts = Post.objects.filter(user__in=followed_users).order_by('-created_at')

    # Serialize the posts and return them
    serialized_posts = PostSerializer(posts, many=True)
    return Response(serialized_posts.data)
