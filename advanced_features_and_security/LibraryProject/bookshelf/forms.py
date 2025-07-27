# bookshelf/forms.py
from django import forms

class BookSearchForm(forms.Form):
    q = forms.CharField(
        required=True,
        max_length=100,
        label='Search',
        widget=forms.TextInput(attrs={'placeholder': 'Title or author'})
    )
