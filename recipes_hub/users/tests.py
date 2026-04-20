import tempfile
from datetime import date

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from django.test import TestCase
from django.urls import reverse

from users.forms import ProfileForm
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

    def test_profile_settings_requires_login(self):
        response = self.client.get(reverse("users:profile_settings"))

        self.assertRedirects(
            response,
            f'{reverse("users:login")}?next={reverse("users:profile_settings")}',
        )

    def test_password_reset_redirects_to_namespaced_done_view(self):
        User.objects.create_user(
            username="chef",
            email="chef@example.com",
            password="StrongPassword123",
        )

        response = self.client.post(
            reverse("users:password_reset"),
            {"email": "chef@example.com"},
        )

        self.assertRedirects(response, reverse("users:password_reset_done"))

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_profile_can_be_updated(self):
        user = User.objects.create_user(
            username="chef",
            email="chef@example.com",
            password="StrongPassword123",
        )
        self.client.login(username="chef", password="StrongPassword123")
        image = SimpleUploadedFile(
            "avatar.gif",
            (
                b"GIF87a\x01\x00\x01\x00\x80\x00\x00"
                b"\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,"
                b"\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;"
            ),
            content_type="image/gif",
        )

        response = self.client.post(
            reverse("users:profile_settings"),
            {
                "username": "chef-updated",
                "email": "updated@example.com",
                "birthday": "1998-03-12",
            },
        )

        self.assertRedirects(response, reverse("users:profile_settings"))
        user.refresh_from_db()
        profile = user.profile
        self.assertEqual(user.username, "chef-updated")
        self.assertEqual(user.email, "updated@example.com")
        self.assertEqual(str(profile.birthday), "1998-03-12")

        upload_response = self.client.post(
            reverse("users:profile"),
            {"image": image},
        )

        self.assertRedirects(upload_response, reverse("users:profile"))
        profile.refresh_from_db()
        self.assertTrue(profile.image.name)

    def test_profile_rejects_future_birthday(self):
        form = ProfileForm(data={"birthday": "2999-01-01"})

        self.assertFalse(form.is_valid())
        self.assertIn("birthday", form.errors)

    def test_profile_rejects_unrealistically_old_birthday(self):
        too_old_year = date.today().year - 121
        form = ProfileForm(data={"birthday": f"{too_old_year}-01-01"})

        self.assertFalse(form.is_valid())
        self.assertIn("birthday", form.errors)
