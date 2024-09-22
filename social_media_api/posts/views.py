from rest_framework import viewsets, permissions
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework import  status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics, status
from django.shortcuts import get_object_or_404
from notifications.models import Notification

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostPagination(PageNumberPagination):
    page_size = 10

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PostPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'content']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_feed(request):
    # Get the users that the current user is following
    following_users = request.user.following.all()
    # Get the posts from the followed users, ordered by creation date
    posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

    # You may want to serialize the posts (assuming you have a PostSerializer)
    from .serializers import PostSerializer
    serialized_posts = PostSerializer(posts, many=True)

    return Response(serialized_posts.data, status=status.HTTP_200_OK)

# View to handle liking a post
@api_view(['POST'])
def like_post(request, pk):
    post = generics.get_object_or_404(Post, pk=pk)  # Ensure the Post exists
    like, created = Like.objects.get_or_create(user=request.user, post=post)  # Handle like creation
    
    if created:
        # Generate notification for the post author
        Notification.objects.create(
            recipient=post.author,
            actor=request.user,
            verb="liked your post",
            target=post
        )
        return Response({'message': 'Post liked and notification created'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'You have already liked this post'}, status=status.HTTP_400_BAD_REQUEST)

# View to handle unliking a post
@api_view(['POST'])
def unlike_post(request, pk):
    post = generics.get_object_or_404(Post, pk=pk)  # Ensure the Post exists
    like = Like.objects.filter(user=request.user, post=post).first()  # Check if the like exists
    
    if like:
        like.delete()  # Delete the like
        return Response({'message': 'Post unliked'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'You have not liked this post yet'}, status=status.HTTP_400_BAD_REQUEST)