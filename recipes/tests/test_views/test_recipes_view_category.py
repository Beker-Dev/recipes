from recipes.tests.recipe_test_base import RecipeTestBase
from django.urls import resolve, reverse
from recipes import views


class TestRecipesViewsCategory(RecipeTestBase):

    def test_recipes_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipes_category_view_function_returns_status_code_404_not_found_if_no_recipes_found(self):
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertEqual(response.status_code, 404)

    def test_recipes_category_view_template_shows_recipes_if_recipes(self):
        title = 'Cookies'
        self.make_recipe(title=title)
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        template_content = response.content.decode('utf-8')
        self.assertIn(title, template_content)

    def test_recipes_category_view_template_does_not_load_recipe_if_not_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': recipe.category.id}))
        self.assertEqual(response.status_code, 404)
