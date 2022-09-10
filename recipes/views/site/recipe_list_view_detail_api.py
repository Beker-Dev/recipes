from .recipe_list_view_detail import RecipeListViewDetail
from recipes.models import Recipe
from django.http import JsonResponse
from django.forms.models import model_to_dict


class RecipeListViewDetailApiV1(RecipeListViewDetail):
    def get_image_url(self, recipe: dict) -> str:
        return self.request.build_absolute_uri()[:-1] + recipe['cover'].url if recipe['cover'] else ''

    def get_json_recipe(self, recipe: Recipe):
        recipe_dict = model_to_dict(recipe)
        recipe_dict['cover'] = self.get_image_url(recipe_dict)
        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)
        recipe_dict.pop('is_published')
        recipe_dict.pop('preparation_steps_is_html')
        return recipe_dict

    def render_to_response(self, *args, **kwargs):
        recipe = self.get_context_data().get('recipe')
        recipe = self.get_json_recipe(recipe)
        return JsonResponse(recipe, safe=False)
