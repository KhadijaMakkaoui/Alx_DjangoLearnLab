from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, PostSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from .models import Post

User = get_user_model()

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = (permissions.AllowAny,)

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    # Fetch all users
    all_users = CustomUser.objects.all()
    
    # Find the user to follow from the list
    user_to_follow = None
    for user in all_users:
        if user.id == user_id:
            user_to_follow = user
            break
    
    if not user_to_follow:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.user == user_to_follow:
        return Response({'error': "You can't follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

    request.user.following.add(user_to_follow)
    return Response({'success': f'You are now following {user_to_follow.username}'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    # Fetch all users
    all_users = CustomUser.objects.all()
    
    # Find the user to unfollow from the list
    user_to_unfollow = None
    for user in all_users:
        if user.id == user_id:
            user_to_unfollow = user
            break
    
    if not user_to_unfollow:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    request.user.following.remove(user_to_unfollow)
    return Response({'success': f'You have unfollowed {user_to_unfollow.username}'}, status=status.HTTP_200_OK)