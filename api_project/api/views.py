from django.shortcuts import render
from rest_framework import generics
from .serializers import BookSerializer
# Create your views here.
class BookList(generics.ListAPIView):
    serializer_class = BookSerializer

