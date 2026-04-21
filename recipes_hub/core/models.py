__all__ = ()

from django.db import models


class IsPublishedModel(models.Model):
    is_published = models.BooleanField(
        default=True,
        verbose_name="опубликовано",
        help_text="Отмечает публикацию объекта.",
    )

    class Meta:
        abstract = True


class NameModel(models.Model):
    name = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="название",
        help_text="Уникальное название объекта.",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата создания",
        help_text="Дата и время создания объекта.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="дата обновления",
        help_text="Дата и время последнего обновления объекта.",
    )

    class Meta:
        abstract = True
