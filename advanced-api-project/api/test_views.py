from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book


class BookAPITestCase(APITestCase):
    """Comprehensive tests for Book API endpoints."""

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password123")

        # Create an author
        self.author = Author.objects.create(name="Test Author")

        # Create some books
        self.book1 = Book.objects.create(
            title="Book One", publication_year=2020, author=self.author
        )
        self.book2 = Book.objects.create(
            title="Book Two", publication_year=2021, author=self.author
        )

        # Endpoints
        self.list_url = reverse('book-list')      # /books/
        self.detail_url = reverse('book-detail', args=[self.book1.id])
        self.create_url = reverse('book-create')  # /books/create/
        self.update_url = reverse('book-update')  # /books/update/
        self.delete_url = reverse('book-delete')  # /books/delete/

    # ---------- CRUD TESTS ----------

    def test_list_books(self):
        """Test retrieving all books (public)."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_single_book(self):
        """Test retrieving a single book by ID."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    def test_create_book_authenticated(self):
        """Test creating a book when logged in."""
        self.client.login(username="testuser", password="password123")
        data = {
            "title": "New Book",
            "publication_year": 2022,
            "author": self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        """Test creating a book without logging in."""
        data = {
            "title": "New Book",
            "publication_year": 2022,
            "author": self.author.id
        }
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authenticated(self):
        """Test updating a book when logged in."""
        self.client.login(username="testuser", password="password123")
        data = {"id": self.book1.id, "title": "Updated Book", "publication_year": 2020, "author": self.author.id}
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Book")

    def test_delete_book_authenticated(self):
        """Test deleting a book when logged in."""
        self.client.login(username="testuser", password="password123")
        data = {"id": self.book1.id}
        response = self.client.delete(self.delete_url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    # ---------- FILTER / SEARCH / ORDER TESTS ----------

    def test_filter_books_by_title(self):
        """Test filtering books by title."""
        response = self.client.get(f"{self.list_url}?title=Book One")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Book One")

    def test_search_books(self):
        """Test searching books by keyword."""
        response = self.client.get(f"{self.list_url}?search=Two")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Book Two")

    def test_order_books_by_year_desc(self):
        """Test ordering books by publication year descending."""
        response = self.client.get(f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2021)
