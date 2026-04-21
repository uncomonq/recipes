__all__ = ()

from django.utils.translation import get_language
from django.views.generic import TemplateView
from recipes.models import Recipe

COURSE_LABELS = {
    "first": {
        "en": "First course",
        "ru": "Первое",
    },
    "second": {
        "en": "Main course",
        "ru": "Второе",
    },
    "third": {
        "en": "Third course",
        "ru": "Третье",
    },
    "salad": {
        "en": "Salad",
        "ru": "Салат",
    },
}

HOME_TEXT = {
    "en": {
        "hero_title": "Find the Perfect Recipe",
        "hero_subtitle": "Discover delicious meals for any occasion.",
        "hero_button": "Go to Recipe search",
        "popular_title": "Popular Recipes",
        "popular_subtitle": "Try these delicious dishes",
        "view_all_button": "View All Recipes",
        "cook_time_suffix": "min",
        "rating_label": "Rating",
        "spice_label": "Spice level",
    },
    "ru": {
        "hero_title": "Найдите идеальный рецепт",
        "hero_subtitle": "Открывайте вкусные блюда для любого случая.",
        "hero_button": "Перейти к поиску рецептов",
        "popular_title": "Популярные рецепты",
        "popular_subtitle": "Попробуйте эти вкусные блюда",
        "view_all_button": "Смотреть все рецепты",
        "cook_time_suffix": "мин",
        "rating_label": "Рейтинг",
        "spice_label": "Острота",
    },
}


def _current_language():
    language = (get_language() or "en").split("-")[0]
    return language if language in HOME_TEXT else "en"


def _course_label(slug, language):
    if slug not in COURSE_LABELS:
        return ""
    return COURSE_LABELS[slug][language]


def _recipe_image_url(recipe):
    image = next(iter(recipe.images.all()), None)
    if image is None or not image.image:
        return ""
    try:
        return image.image.url
    except ValueError:
        return ""


class HomeView(TemplateView):
    template_name = "homepage/main.html"

    def _items(self, language):
        recipes = Recipe.objects.filter(is_published=True).prefetch_related(
            "images",
        )
        recipes = recipes.order_by("-rating", "name")[:6]
        return [
            {
                "name": recipe.name,
                "duration": (
                    f"{recipe.cook_time} "
                    f"{HOME_TEXT[language]['cook_time_suffix']}"
                ),
                "kind": _course_label(recipe.course, language),
                "image_url": _recipe_image_url(recipe),
                "rating": recipe.rating,
                "rating_label": HOME_TEXT[language]["rating_label"],
                "spice_level": recipe.get_spice_level_display(),
                "spice_label": HOME_TEXT[language]["spice_label"],
            }
            for recipe in recipes
        ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language = _current_language()
        context["items"] = self._items(language)
        context["ui"] = HOME_TEXT[language]
        return context
