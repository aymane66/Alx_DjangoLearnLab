# My input:

from bookshelf.models import Book
books = Book.objects.get(title="1984")
book


# Output:

[<Book: 1984 by George Orwell (1949)>]