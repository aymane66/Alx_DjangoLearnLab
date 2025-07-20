from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

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
]

