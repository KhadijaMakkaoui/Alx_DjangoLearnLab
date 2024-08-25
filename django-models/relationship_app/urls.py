from django.urls import path
from .views import *
from django.contrib.auth import views 

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
     # Authentication
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]