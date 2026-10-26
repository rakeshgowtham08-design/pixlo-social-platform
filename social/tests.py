from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Like

class PixloSmokeTests(TestCase):
    def test_feed_loads(self):
        response = self.client.get(reverse("feed"))
        self.assertEqual(response.status_code, 200)

    def test_authenticated_user_can_create_post(self):
        user = User.objects.create_user(username="pixlo_tester", password="strong-test-pass-123")
        self.client.login(username="pixlo_tester", password="strong-test-pass-123")
        response = self.client.post(reverse("create_post"), {"caption": "Hello Pixlo!"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(author=user, caption="Hello Pixlo!").exists())
