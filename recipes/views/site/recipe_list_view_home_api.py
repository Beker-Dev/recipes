from .recipe_list_view_home import RecipeListViewHome
from django.http import JsonResponse


class RecipeListViewHomeApiV1(RecipeListViewHome):
    def get_image_url(self, recipe: dict) -> str:
        return self.request.build_absolute_uri() + recipe['cover'] if recipe['cover'] else ''

    def get_json_recipes(self, recipes: list) -> list:
        recipes_list = list(recipes)
        for recipe in recipes_list:
            recipe['cover'] = self.get_image_url(recipe)
            recipe.pop('is_published')
            recipe.pop('preparation_steps_is_html')
        return recipes_list

    def render_to_response(self, *args, **kwargs):
        recipes = self.get_context_data().get('recipes').values()
        recipes = self.get_json_recipes(recipes)
        return JsonResponse(recipes, safe=False)

