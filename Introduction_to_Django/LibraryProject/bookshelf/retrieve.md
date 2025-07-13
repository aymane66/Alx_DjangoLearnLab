# My input:

from bookshelf.models import Book
books = Book.objects.all()
list(books)


# Output:

[<Book: 1984 by George Orwell (1949)>]