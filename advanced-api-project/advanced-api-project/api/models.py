from django.db import models

# Create your models here.

# The Author model stores the name of the author
class Author(models.Model):
    name= models.CharField(max_length=255)

    def __str__(self):
        return self.name

# The Book model stores a book's title, publication year, and the author it belongs to
class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title