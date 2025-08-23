from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Comment


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass123")
        self.post = Post.objects.create(
            title="Test Post", content="Post content", author=self.user
        )
        self.comment = Comment.objects.create(
            post=self.post, author=self.user, content="This is a test comment"
        )

    def test_comment_str(self):
        """Check string representation of comment"""
        self.assertEqual(str(self.comment), "Comment by tester on Test Post")

    def test_comment_belongs_to_post(self):
        """Check comment is linked to the right post"""
        self.assertEqual(self.comment.post, self.post)


class CommentViewTest(TestCase):
    def setUp(self):
        # create users
        self.user1 = User.objects.create_user(username="user1", password="pass123")
        self.user2 = User.objects.create_user(username="user2", password="pass123")

        # create post
        self.post = Post.objects.create(
            title="Another Post", content="Some content", author=self.user1
        )

        # create comment
        self.comment = Comment.objects.create(
            post=self.post, author=self.user1, content="User1's comment"
        )

    def test_comments_visible_on_post_detail(self):
        """Anyone can see comments under a post"""
        response = self.client.get(reverse("post-detail", args=[self.post.id]))
        self.assertContains(response, "User1's comment")

    def test_logged_in_user_can_add_comment(self):
        """Authenticated users can add comments"""
        self.client.login(username="user2", password="pass123")
        response = self.client.post(
            reverse("add-comment", args=[self.post.id]),
            {"content": "User2's new comment"},
            follow=True,
        )
        self.assertContains(response, "User2's new comment")
        self.assertEqual(Comment.objects.count(), 2)

    def test_only_author_can_edit_comment(self):
        """Only comment author can edit"""
        self.client.login(username="user2", password="pass123")
        response = self.client.post(
            reverse("edit-comment", args=[self.comment.id]),
            {"content": "Trying to edit"},
        )
        self.assertEqual(response.status_code, 403)  # forbidden

        # now try as correct author
        self.client.login(username="user1", password="pass123")
        response = self.client.post(
            reverse("edit-comment", args=[self.comment.id]),
            {"content": "Updated by author"},
            follow=True,
        )
        self.assertContains(response, "Updated by author")

    def test_only_author_can_delete_comment(self):
        """Only comment author can delete"""
        self.client.login(username="user2", password="pass123")
        response = self.client.post(reverse("delete-comment", args=[self.comment.id]))
        self.assertEqual(response.status_code, 403)  # forbidden
        self.assertEqual(Comment.objects.count(), 1)

        # correct author deletes
        self.client.login(username="user1", password="pass123")
        response = self.client.post(reverse("delete-comment", args=[self.comment.id]))
        self.assertRedirects(response, reverse("post-detail", args=[self.post.id]))
        self.assertEqual(Comment.objects.count(), 0)
