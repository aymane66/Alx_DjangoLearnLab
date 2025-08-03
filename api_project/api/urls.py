from django.urls import path, include
from .views import BookList, BookViewSet, CustomAuthToken
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),
    path("", include(router.urls)),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth')
]