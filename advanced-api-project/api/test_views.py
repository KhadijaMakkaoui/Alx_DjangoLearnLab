from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Author, Book
from django.contrib.auth.models import User

class BookAPITestCase(APITestCase):
    def setUp(self):
        """Set up initial data and authentication for testing."""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        self.author = Author.objects.create(name="J.K. Rowling")
        self.book = Book.objects.create(title="Harry Potter", publication_year=1997, author=self.author)

    def test_create_book(self):
        """Test creating a new book via POST request."""
        url = reverse('book-list')
        data = {
            "title": "New Book",
            "publication_year": 2023,
            "author": self.author.id
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.last().title, "New Book")

    def test_update_book(self):
        """Test updating an existing book via PUT request."""
        url = reverse('book-detail', args=[self.book.id])
        data = {
            "title": "Updated Book",
            "publication_year": 1998,
            "author": self.author.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, "Updated Book")

    def test_delete_book(self):
        """Test deleting a book via DELETE request."""
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_filter_books_by_title(self):
        """Test filtering books by title."""
        url = reverse('book-list') + '?title=Harry Potter'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Harry Potter")

    def test_search_books_by_author(self):
        """Test searching books by author."""
        url = reverse('book-list') + '?search=Rowling'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], self.author.id)

    def test_order_books_by_year(self):
        """Test ordering books by publication year."""
        url = reverse('book-list') + '?ordering=publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 1997)

    def test_permissions(self):
        """Test that book creation, update, and delete are restricted to authenticated users."""
        self.client.logout()
        
        # Test create without authentication
        url = reverse('book-list')
        data = {"title": "Unauthorized Book", "publication_year": 2021, "author": self.author.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test update without authentication
        url = reverse('book-detail', args=[self.book.id])
        response = self.client.put(url, data={"title": "Unauthorized Update"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Test delete without authentication
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)