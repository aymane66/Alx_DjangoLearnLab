from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AuthTests(TestCase):

    def test_register_user(self):
        response = self.client.post(reverse("register"), {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "strongpassword123",
            "password2": "strongpassword123",
        })
        self.assertEqual(response.status_code, 302)  # redirect after success
        self.assertTrue(User.objects.filter(username="testuser").exists())


    def test_login(self):
        user = User.objects.create_user(username="tester", email="t@t.com", password="testpass123")
        response = self.client.post(reverse("login"), {
            "username": "tester",
            "password": "testpass123",
        })
        self.assertEqual(response.status_code, 302)  # login success redirects
