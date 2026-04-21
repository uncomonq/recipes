__all__ = ()

from django.shortcuts import redirect
from django.utils.translation import get_language
from django.views.generic import TemplateView
from recipes.models import Ingredient
from recipes.models import Recipe

SESSION_ITEMS_KEY = "ingredient_search_items"
SESSION_COURSE_KEY = "ingredient_search_course"

VALID_COURSES = frozenset(value for value, _ in Recipe.Course.choices)

DEFAULT_INGREDIENT_EMOJI = "🍽️"

INGREDIENT_EMOJIS = {
    "говядина": "🥩",
    "горчица": "🌿",
    "зелень": "🌿",
    "капуста": "🥬",
    "картофель": "🥔",
    "креветки": "🦐",
    "куриное мясо": "🍗",
    "лавровый лист": "🌿",
    "лук репчатый": "🧅",
    "масло растительное": "🛢️",
    "масло сливочное": "🧈",
    "молоко": "🥛",
    "морковь": "🥕",
    "мука": "🌾",
    "огурцы": "🥒",
    "помидоры": "🍅",
    "свёкла": "🟣",
    "сливки": "🥛",
    "сметана": "🥛",
    "соль": "🧂",
    "сосиски": "🌭",
    "вермишель": "🍜",
    "вешенки": "🍄",
    "шампиньоны": "🍄",
    "яйца": "🥚",
}

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

COURSE_EMOJIS = {
    "first": "🍲",
    "second": "🍛",
    "third": "🍰",
    "salad": "🥗",
}

FIND_UI = {
    "en": {
        "page_title": "Find Recipes",
        "hero_title": "Select Ingredients You Have",
        "hero_subtitle": "Find recipes based on what's in your fridge.",
        "search_placeholder": "Search for ingredients...",
        "search_button": "Search",
        "find_recipes_button": "Find Recipes",
        "filter_course_label": "Dish type",
        "course_chip_prefix": "Dish:",
        "no_course": "Not selected",
        "no_ingredients": "None yet - tap ingredients below",
        "clear_course": "Clear dish type",
    },
    "ru": {
        "page_title": "Поиск рецептов",
        "hero_title": "Выберите ингредиенты",
        "hero_subtitle": ("Найдите рецепты из того, что есть в холодильнике."),
        "search_placeholder": "Поиск ингредиентов...",
        "search_button": "Искать",
        "find_recipes_button": "Найти рецепты",
        "filter_course_label": "Тип блюда",
        "course_chip_prefix": "Блюдо:",
        "no_course": "Не выбрано",
        "no_ingredients": "Пока нет - нажмите ингредиенты ниже",
        "clear_course": "Сбросить тип блюда",
    },
}

RESULTS_UI = {
    "en": {
        "page_title": "Search Results",
        "title": "Recipes for your ingredients",
        "subtitle": "Selected ingredients:",
        "search_placeholder": "Refine search...",
        "edit_button": "Edit ingredients",
        "found_text": "Found",
        "for_you": "recipes for you",
        "sort_by": "Sort by",
        "sort_placeholder": "Fewest missing ingredients",
        "no_results": "No recipes matched. Try other ingredients.",
        "all_ingredients": "All ingredients are available",
        "missing_prefix": "Missing",
        "missing_suffix": "ingredient(s)",
        "cook_time_suffix": "min",
        "rating_label": "Rating",
        "spice_label": "Spice level",
    },
    "ru": {
        "page_title": "Результаты поиска",
        "title": "Рецепты по вашим ингредиентам",
        "subtitle": "Выбранные ингредиенты:",
        "search_placeholder": "Уточнить поиск...",
        "edit_button": "Редактировать",
        "found_text": "Найдено",
        "for_you": "рецептов для вас",
        "sort_by": "Сортировать",
        "sort_placeholder": "Меньше недостающих ингредиентов",
        "no_results": "Ничего не найдено. Попробуйте другие ингредиенты.",
        "all_ingredients": "Все ингредиенты есть",
        "missing_prefix": "Не хватает",
        "missing_suffix": "ингредиента(ов)",
        "cook_time_suffix": "мин",
        "rating_label": "Рейтинг",
        "spice_label": "Острота",
    },
}


def _current_language():
    language = (get_language() or "en").split("-")[0]
    return language if language in FIND_UI else "en"


def _course_label(slug, language):
    if slug not in COURSE_LABELS:
        return ""
    return f"{COURSE_EMOJIS[slug]} {COURSE_LABELS[slug][language]}"


def _course_types(language):
    return [
        {
            "slug": slug,
            "title": _course_label(slug, language),
            "active": False,
        }
        for slug in VALID_COURSES
    ]


def _display_ingredient(name):
    emoji = INGREDIENT_EMOJIS.get(name.lower(), DEFAULT_INGREDIENT_EMOJI)
    return f"{emoji} {name}"


def _raw_ingredient_name(value):
    name = value.strip()
    if name and not name[0].isalnum() and " " in name:
        return name.split(" ", maxsplit=1)[1].strip()
    return name


def _ingredient_names():
    return list(
        Ingredient.objects.order_by("name").values_list("name", flat=True),
    )


def _ingredient_items():
    return [
        {
            "name": name,
            "label": _display_ingredient(name),
        }
        for name in _ingredient_names()
        if name
    ]


def _ingredient_choices():
    return frozenset(_ingredient_names())


def _selected_ingredients(values):
    choices = _ingredient_choices()
    selected = []
    for value in values:
        name = _raw_ingredient_name(value)
        if name in choices and name not in selected:
            selected.append(name)
    return selected


def _ingredient_labels(names):
    return [_display_ingredient(name) for name in names]


def _recipe_image_url(recipe):
    image = next(iter(recipe.images.all()), None)
    if image is None or not image.image:
        return ""
    try:
        return image.image.url
    except ValueError:
        return ""


class FindByIngredientsView(TemplateView):
    template_name = "ingredient_search/find.html"

    def get(self, request, *args, **kwargs):
        if "course" in request.GET:
            raw = (request.GET.get("course") or "").strip()
            if raw in VALID_COURSES:
                current = request.session.get(SESSION_COURSE_KEY)
                if current == raw:
                    request.session.pop(SESSION_COURSE_KEY, None)
                else:
                    request.session[SESSION_COURSE_KEY] = raw
            else:
                request.session.pop(SESSION_COURSE_KEY, None)
            request.session.modified = True
            return redirect("recipes:list")

        if "toggle" in request.GET:
            toggle = _raw_ingredient_name(request.GET.get("toggle") or "")
            if toggle in _ingredient_choices():
                items = list(request.session.get(SESSION_ITEMS_KEY, []))
                if toggle in items:
                    items.remove(toggle)
                else:
                    items.append(toggle)
                request.session[SESSION_ITEMS_KEY] = items
                request.session.modified = True
            return redirect("recipes:list")

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language = _current_language()
        ui = FIND_UI[language]
        selected_course = self.request.session.get(SESSION_COURSE_KEY) or ""
        if selected_course not in VALID_COURSES:
            selected_course = ""

        selected_items = _selected_ingredients(
            self.request.session.get(SESSION_ITEMS_KEY, []),
        )
        self.request.session[SESSION_ITEMS_KEY] = selected_items

        course_types = []
        for row in _course_types(language):
            course_types.append(
                {
                    **row,
                    "active": row["slug"] == selected_course,
                },
            )

        context["ui"] = ui
        context["course_types"] = course_types
        context["ingredients"] = _ingredient_items()
        context["selected_items"] = selected_items
        context["selected_badges"] = _ingredient_labels(selected_items)
        context["selected_course"] = selected_course
        context["selected_course_label"] = _course_label(
            selected_course,
            language,
        )
        return context


class SearchResultsView(TemplateView):
    template_name = "ingredient_search/results.html"

    def _selected_items(self, request):
        from_post = _selected_ingredients(
            request.POST.getlist("ingredients"),
        )
        if from_post:
            return from_post
        return _selected_ingredients(
            request.session.get(SESSION_ITEMS_KEY, []),
        )

    def _selected_course(self, request):
        raw = (request.POST.get("course") or "").strip()
        if raw in VALID_COURSES:
            return raw
        session_course = request.session.get(SESSION_COURSE_KEY) or ""
        return session_course if session_course in VALID_COURSES else ""

    def _query(self, request):
        return (request.POST.get("q") or "").strip()

    def _recipe_items(self, language):
        recipes = Recipe.objects.filter(is_published=True).prefetch_related(
            "images",
            "recipe_ingredients__ingredient",
        )
        return [
            {
                "name": recipe.name,
                "duration": (
                    f"{recipe.cook_time} "
                    f"{RESULTS_UI[language]['cook_time_suffix']}"
                ),
                "kind": _course_label(recipe.course, language),
                "ingredients": ingredients,
                "course": recipe.course,
                "image_url": _recipe_image_url(recipe),
                "rating": recipe.rating,
                "rating_label": RESULTS_UI[language]["rating_label"],
                "spice_level": recipe.get_spice_level_display(),
                "spice_label": RESULTS_UI[language]["spice_label"],
            }
            for recipe in recipes
            for ingredients in [
                [
                    item.ingredient.name
                    for item in recipe.recipe_ingredients.all()
                ],
            ]
        ]

    def _course_matches(self, recipe, selected_course):
        if not selected_course:
            return True
        return recipe["course"] == selected_course

    def _query_matches(self, recipe, query):
        if not query:
            return True
        lowered = query.lower()
        if lowered in recipe["name"].lower():
            return True
        if lowered in recipe["kind"].lower():
            return True
        return any(
            lowered in ingredient.lower()
            for ingredient in recipe["ingredients"]
        )

    def _missing_text(self, missing_count, ui):
        if missing_count <= 0:
            return ui["all_ingredients"]
        return (
            f'{ui["missing_prefix"]} {missing_count} '
            f'{ui["missing_suffix"]}'
        )

    def _filter_recipes(
        self,
        recipes,
        selected_items,
        selected_course,
        query,
        ui,
    ):
        ranked = []
        selected_set = set(selected_items)
        for recipe in recipes:
            recipe_ingredients = set(recipe["ingredients"])
            overlap_count = len(selected_set & recipe_ingredients)
            if selected_set and overlap_count == 0:
                continue
            if not self._course_matches(recipe, selected_course):
                continue
            if not self._query_matches(recipe, query):
                continue

            missing_count = len(recipe_ingredients - selected_set)
            recipe_data = {
                **recipe,
                "missing_count": missing_count,
                "missing_text": self._missing_text(missing_count, ui),
            }
            ranked.append(
                (missing_count, -overlap_count, recipe["name"], recipe_data),
            )

        ranked.sort(key=lambda row: (row[0], row[1], row[2]))
        return [row[3] for row in ranked]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language = _current_language()
        ui = RESULTS_UI[language]
        request = self.request
        selected_items = self._selected_items(request)
        selected_course = self._selected_course(request)
        query = self._query(request)
        recipes = self._recipe_items(language)
        filtered = self._filter_recipes(
            recipes,
            selected_items,
            selected_course,
            query,
            ui,
        )

        context["ui"] = ui
        context["selected_items"] = selected_items
        context["selected_badges"] = _ingredient_labels(selected_items)
        context["selected_course"] = selected_course
        context["selected_course_label"] = _course_label(
            selected_course,
            language,
        )
        context["query"] = query
        context["recipes"] = filtered
        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
