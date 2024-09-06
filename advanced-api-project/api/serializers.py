from rest_framework import serializers
from .models import Author, Book
from datetime import date

# The BookSerializer serializes the book model, ensuring the publication year is not in the future.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']
    # Custom validation to ensure publication_year is not in the future
    def validate_publication_year(self, value):
        if value > date.today().year:
            raise serializers.ValidationError("Publication year cannot be in the future.") 
        return value
    
# The AuthorSerializer includes the author's name and a nested BookSerializer to serialize the related books.
class AuthorSerializer(serializers.ModelSerializer):
    #Nested BookSerializer
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name' , 'books']