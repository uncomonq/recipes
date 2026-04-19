from django.conf import settings
from django.db import models


def profile_image_path(instance, filename):
    return f"users/{instance.user.id}/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    birthday = models.DateField(
        null=True,
        blank=True,
        verbose_name="birthday",
    )
    image = models.ImageField(
        upload_to=profile_image_path,
        null=True,
        blank=True,
        verbose_name="avatar",
    )

    class Meta:
        verbose_name = "profile"
        verbose_name_plural = "profiles"

    def __str__(self):
        return f"Profile for {self.user.username}"
