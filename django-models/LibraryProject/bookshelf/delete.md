# My input:

from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
book

# Output:

(1, {'bookshelf.Book': 1})
