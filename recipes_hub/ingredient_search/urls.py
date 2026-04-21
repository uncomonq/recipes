__all__ = ()

from django.urls import path
from ingredient_search.views import FindByIngredientsView, SearchResultsView

app_name = "recipes"

urlpatterns = [
    path("", FindByIngredientsView.as_view(), name="list"),
    path("results/", SearchResultsView.as_view(), name="results"),
]
