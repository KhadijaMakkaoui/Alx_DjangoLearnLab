from rest_framework import serializers
from .models import Book
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author'] #or use  fields = '__all__' to include all
