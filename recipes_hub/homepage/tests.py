# __all__ = ()

# from http import HTTPStatus
#
# from django.contrib.auth import get_user_model
# from django.test import override_settings
# from django.test import TestCase
# from django.urls import reverse
#
# from catalog.models import Category
# from catalog.models import Item
# from catalog.models import Tag
# from homepage.forms import EchoForm
# from lyceum.middleware import ReverseRussianWordsMiddleware
#
#
# class StaticURLTests(TestCase):
#    def setUp(self):
#        ReverseRussianWordsMiddleware.request_counter = 0
#
#    def test_homepage_endpoint(self):
#        response = self.client.get(reverse("homepage:home"))
#        self.assertEqual(response.status_code, HTTPStatus.OK)
#
#    def test_coffee(self):
#        response = self.client.get(reverse("homepage:coffee_slash"))
#        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
#        self.assertEqual(response.content.decode(), "Я чайник")
#
#    def test_admin_link_hidden_for_anonymous_user(self):
#        response = self.client.get(reverse("homepage:home"))
#        self.assertEqual(response.status_code, HTTPStatus.OK)
#        self.assertNotContains(response, 'href="/admin/"')
#
#    def test_admin_link_visible_for_staff_user(self):
#        user_model = get_user_model()
#        user_model.objects.create_user(
#            username="staff_user",
#            password="password123",
#            is_staff=True,
#        )
#        self.client.login(username="staff_user", password="password123")
#        response = self.client.get(reverse("homepage:home"))
#        self.assertEqual(response.status_code, HTTPStatus.OK)
#        self.assertContains(response, 'href="/admin/"')
#
#
# class HomepageContextTests(TestCase):
#    @classmethod
#    def setUpTestData(cls):
#        category = Category.objects.create(
#            name="Home category",
#            slug="home-category",
#            weight=100,
#        )
#        hidden_category = Category.objects.create(
#            name="Hidden category",
#            slug="hidden-category",
#            is_published=False,
#            weight=200,
#        )
#        public_tag = Tag.objects.create(
#            name="Public tag",
#            slug="public-tag",
#        )
#        hidden_tag = Tag.objects.create(
#            name="Hidden tag",
#            slug="hidden-tag",
#            is_published=False,
#        )
#        cls.item_a = Item.objects.create(
#            name="Alpha",
#            text="First homepage item text.",
#            category=category,
#            is_on_main=True,
#        )
#        cls.item_a.tags.set((public_tag, hidden_tag))
#        cls.item_b = Item.objects.create(
#            name="Beta",
#            text="Second homepage item text.",
#            category=category,
#            is_on_main=True,
#        )
#        cls.item_b.tags.set((public_tag,))
#        cls.item_not_main = Item.objects.create(
#            name="Gamma",
#            text="Item not on main page.",
#            category=category,
#            is_on_main=False,
#        )
#        cls.item_hidden = Item.objects.create(
#            name="Delta",
#            text="Item from hidden category.",
#            category=hidden_category,
#            is_on_main=True,
#        )
#
#    def test_homepage_context_contains_only_main_items(self):
#        response = self.client.get(reverse("homepage:home"))
#        self.assertEqual(response.status_code, HTTPStatus.OK)
#        self.assertIn("items", response.context)
#
#        items = list(response.context["items"])
#        self.assertEqual([item.name for item in items], ["Alpha", "Beta"])
#        self.assertEqual(
#            {tag.name for tag in items[0].tags.all()},
#            {"Public tag"},
#        )
#        self.assertEqual(
#            {tag.name for tag in items[1].tags.all()},
#            {"Public tag"},
#        )
#
#    def test_homepage_context_deferred_item_fields(self):
#        response = self.client.get(reverse("homepage:home"))
#        item = response.context["items"][0]
#        self.assertIn("is_published", item.get_deferred_fields())
#        self.assertIn("is_on_main", item.get_deferred_fields())
#
#    def test_homepage_context_does_not_load_images(self):
#        response = self.client.get(reverse("homepage:home"))
#        item = response.context["items"][0]
#        prefetched = getattr(item, "_prefetched_objects_cache", {})
#        self.assertNotIn("images", prefetched)
#        self.assertNotIn("main_image", item._state.fields_cache)
#
#    def test_homepage_context_loads_only_public_tags_required_fields(self):
#        response = self.client.get(reverse("homepage:home"))
#        item = response.context["items"][0]
#        tag = item.tags.all()[0]
#        self.assertEqual(tag.name, "Public tag")
#        self.assertIn("is_published", tag.get_deferred_fields())
#        self.assertIn("slug", tag.get_deferred_fields())
#
#
# @override_settings(ALLOW_REVERSE=False)
# class EchoTests(TestCase):
#    def setUp(self):
#        ReverseRussianWordsMiddleware.request_counter = 0
#
#    def test_echo_page_contains_form(self):
#        response = self.client.get(reverse("homepage:echo"))
#
#        self.assertEqual(response.status_code, HTTPStatus.OK)
#        self.assertIn("form", response.context)
#        self.assertIsInstance(response.context["form"], EchoForm)
#
#    def test_echo_submit_returns_plaintext(self):
#        response = self.client.post(
#            reverse("homepage:echo_submit"),
#            data={"text": "Привет, Django!"},
#        )
#
#        self.assertEqual(response.status_code, HTTPStatus.OK)
#        self.assertEqual(response.content.decode(), "Привет, Django!")
#        self.assertEqual(
#            response["Content-Type"],
#            "text/plain; charset=utf-8",
#        )
#
#    def test_echo_submit_is_post_only(self):
#        response = self.client.get(reverse("homepage:echo_submit"))
#        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
#
#    def test_echo_page_is_get_only(self):
#        response = self.client.post(reverse("homepage:echo"))
#        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
