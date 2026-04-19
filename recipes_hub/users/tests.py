from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from users.models import Profile


class UsersAuthTests(TestCase):
    def test_signup_creates_user_and_profile(self):
        response = self.client.post(
            reverse("users:signup"),
            {
                "username": "chef",
                "email": "chef@example.com",
                "first_name": "Chef",
                "last_name": "Cook",
                "password1": "StrongPassword123",
                "password2": "StrongPassword123",
            },
        )

        self.assertRedirects(response, reverse("users:profile"))
        user = User.objects.get(username="chef")
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_profile_requires_login(self):
        response = self.client.get(reverse("users:profile"))

        self.assertRedirects(
            response,
            f'{reverse("users:login")}?next={reverse("users:profile")}',
        )
