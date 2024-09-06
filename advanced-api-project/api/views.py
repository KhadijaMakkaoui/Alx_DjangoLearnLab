from django.shortcuts import render
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters import rest_framework
from django_filters.rest_framework import filters

# Create your views here.

# BookListView: Handles retrieving a list of all books.
# Permission: Allows read-only access to unauthenticated users.
# BookListView: Handles retrieving a list of all books.
# Filtering: Allows filtering by title, author name, and publication year.
# Searching: Allows searching by title and author name.
# Ordering: Allows ordering by title and publication year.
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter,filters.OrderingFilter]
    # Enable filtering by title, author name, and publication year
    filterset_fields = ['title', 'author__name', 'publication_year']  
    # Enable searching by title and author name
    search_fields = ['title', 'author__name']  
    # Allow ordering by title and publication year
    ordering_fields = ['title', 'publication_year']  


class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Additional custom logic can be placed here
        serializer.save()

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    def perform_update(self, serializer):
        # Additional custom logic can be placed here
        serializer.save()

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

