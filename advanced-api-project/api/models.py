from django.db import models


class Author(models.Model):
    # Represents an author with a name field
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    # Represents a book with a title, publication year, and a link to its author
    title = models.CharField(max_length=100)
    publication_year = models.IntegerField()  # Year the book was published
    # ForeignKey creates a many-to-one relationship: many books can belong to one author
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title
