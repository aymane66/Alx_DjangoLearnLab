from rest_framework import serializers
from .models import Author, Book
from datetime import date



class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Serializes all fields of Book.
    Includes validation to ensure publication_year is not in the future.
    """
    class Meta:
        model = Book
        fields = '__all__'

    def validate_publication_year(self, value):
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    Serializes the 'name' field.
    Includes a nested list of books by using BookSerializer.
    The nested 'books' field is read-only and shows all books related to the author.
    This uses the 'related_name' from the Book model to access related books.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['name', 'books']
