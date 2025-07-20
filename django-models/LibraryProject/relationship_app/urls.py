from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import admin_view, librarian_view, member_view

urlpatterns = [
    # Book listing view (function-based)
    path('books/', views.list_books, name='list_books'),

    # Library detail view (class-based)
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # Authentication views (custom registration)
    path('register/', views.register, name='register'),

    # Use Django’s built-in login/logout views with template override
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    path('admin-role/', admin_view, name='admin_view'),
    path('librarian-role/', librarian_view, name='librarian_view'),
    path('member-role/', member_view, name='member_view'),
]

