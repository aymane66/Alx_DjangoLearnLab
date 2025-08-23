from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from .forms import CustomUserCreationForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment
from django.views.generic import ListView, DetailView, CreateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .forms import CommentForm
from django.db.models import Q


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("profile")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("profile")
    else:
        form = UserUpdateForm(instance=request.user)

    return render(request, "registration/profile.html", {"form": form})


## Post CRUD ##

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'   # tell Django where our template is
    context_object_name = 'posts'           # so we can say "posts" instead of "object_list"


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context["comments"] = post.comments.all()  # all comments for this post
        context["form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        """Handle comment form submission"""
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect("post-detail", pk=self.object.pk)
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create_post.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        # set the author automatically to the logged-in user
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    


## Comment CRUD ##

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        # get the post this comment belongs to
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


##



class SearchResultsView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'

    def get_queryset(self):
        q = (self.request.GET.get('q') or '').strip()
        if not q:
            return Post.objects.none()
        return (
            Post.objects.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q) |
                Q(tags__name__icontains=q)
            )
            .distinct()
            .select_related('author')
            .prefetch_related('tags')
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['query'] = self.request.GET.get('q', '')
        return ctx



class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/post_list_by_tag.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.tag = Tag.objects.get(slug=self.kwargs['tag_slug'])
        return Post.objects.filter(tags=self.tag).select_related('author').prefetch_related('tags')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context
