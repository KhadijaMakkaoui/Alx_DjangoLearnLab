from django.urls import path, include
from .views import BookList,BookViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


# Create a router and register the BookViewSet
router = DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('book_list/', BookList.as_view() , name='book-list'),
    path('', include(router.urls)),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),


]
