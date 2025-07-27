# bookshelf/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q

from .models import Book
from .forms import BookSearchForm, BookForm

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    # ORM query only:
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_search(request):
    form = BookSearchForm(request.GET or None)
    books = Book.objects.none()
    if form.is_valid():
        q = form.cleaned_data['q']
        # ORM parameterized filters — no risk of SQL injection
        books = Book.objects.filter(Q(title__icontains=q) | Q(author__icontains=q))
    return render(request, 'bookshelf/book_search.html', {
        'form': form,
        'books': books,
    })

@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():  # ensures data is cleaned
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'bookshelf/book_form.html', {'form': form})

# … similarly for edit / delete with get_object_or_404() and form.is_valid() …
