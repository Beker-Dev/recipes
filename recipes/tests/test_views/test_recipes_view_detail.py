from recipes.tests.recipe_test_base import RecipeTestBase
from django.urls import resolve, reverse
from recipes import views
import unittest


class TestRecipesViewsDetail(RecipeTestBase):
    def test_recipes_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:detail', kwargs={'pk': 1}))
        self.assertIs(view.func, views.detail)

    # @unittest.skip('This method will not be executed')  -- this will skip method below
    def test_recipes_detail_view_function_returns_status_code_404_not_found_if_no_recipe_found(self):
        response = self.client.get(reverse('recipes:detail', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 404)

    def test_recipes_detail_view_template_shows_recipes_if_recipe(self):
        title = 'Fast Food'
        self.make_recipe(title=title)
        response = self.client.get(reverse('recipes:detail', kwargs={'pk': 1}))
        template_content = response.content.decode('utf-8')
        self.assertIn(title, template_content)

    def test_recipes_detail_view_template_does_not_load_recipe_if_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:detail', kwargs={'pk': recipe.id}))
        self.assertEqual(response.status_code, 404)
