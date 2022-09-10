from .recipe_list_view_base import RecipeListViewBase


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

