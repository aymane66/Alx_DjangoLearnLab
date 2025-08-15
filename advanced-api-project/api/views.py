from rest_framework import generics
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


# ListView: Retrieve all books
class BookListView(generics.ListAPIView):
    """
    GET: Returns a list of all books in the system.
    Accessible to all users, no authentication required.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Read-only for everyone


# DetailView: Retrieve a single book by ID
class BookDetailView(generics.RetrieveAPIView):
    """
    GET: Returns details for a specific book by ID.
    Accessible to all users, no authentication required.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# CreateView: Add a new book
class BookCreateView(generics.CreateAPIView):
    """
    POST: Creates a new book.
    Only authenticated users can create.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Example: attach logged-in user as author if you had a user foreign key
        serializer.save()



# UpdateView: Modify an existing book
class BookUpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH: Updates an existing book by ID.
    Only authenticated users can update.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


# DeleteView: Remove a book
class BookDeleteView(generics.DestroyAPIView):
    """
    DELETE: Deletes an existing book by ID.
    Only authenticated users can delete.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
