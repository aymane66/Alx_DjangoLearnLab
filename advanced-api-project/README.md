# Book API — Django REST Framework

## Endpoints
- **GET /api/books/** → List all books (public)
- **GET /api/books/<id>/** → Retrieve single book (public)
- **POST /api/books/create/** → Create new book (authenticated)
- **PUT/PATCH /api/books/<id>/update/** → Update book (authenticated)
- **DELETE /api/books/<id>/delete/** → Delete book (authenticated)

## Permissions
- Public read access for listing and detail.
- Authenticated users required for create, update, delete.

## Custom Behavior
- Validation prevents setting `publication_year` in the future (handled in `BookSerializer`).
