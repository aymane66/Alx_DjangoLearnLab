from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Tag
from django.utils.text import slugify


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email"]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # only the text, post and author handled automatically
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'}),
        }


class PostForm(forms.ModelForm):
    # New: a free-text field the user can type comma-separated tags into
    tags = forms.CharField(
        required=False,
        help_text="Comma-separated, e.g. python, django, tips"
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # author set in the view

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-fill tags when editing: "python, django"
        if self.instance and self.instance.pk:
            current = self.instance.tags.values_list('name', flat=True)
            self.fields['tags'].initial = ', '.join(current)

    def _parse_tags(self, text):
        # split by comma, trim, drop empties, make unique (case-insensitive)
        raw = [t.strip() for t in (text or '').split(',')]
        cleaned = [t for t in raw if t]
        # unique by lowercased name, preserve original casing of first occurrence
        seen = {}
        for t in cleaned:
            key = t.lower()
            if key not in seen:
                seen[key] = t
        return list(seen.values())

    def save(self, commit=True):
        # Save Post first (without M2M) to get an instance
        instance = super().save(commit=False)
        if commit:
            instance.save()

        # Build Tag set from the free-text input
        tag_names = self._parse_tags(self.cleaned_data.get('tags', ''))
        tag_objs = []
        for name in tag_names:
            slug = slugify(name)
            tag, _ = Tag.objects.get_or_create(slug=slug, defaults={'name': name})
            # If tag existed but name casing differs, you may optionally normalize:
            # if tag.name != name: tag.name = name; tag.save()
            tag_objs.append(tag)

        # Assign M2M
        # (must be after instance.save(); commit=False users should handle outside)
        if instance.pk:
            instance.tags.set(tag_objs)
        return instance
