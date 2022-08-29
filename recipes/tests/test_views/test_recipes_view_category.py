from recipes.tests.recipe_test_base import RecipeTestBase
from django.urls import resolve, reverse
from recipes import views


class TestRecipesViewsCategory(RecipeTestBase):

    def test_recipes_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_recipes_category_view_template_shows_recipes_if_recipes(self):
        title = 'Cookies'
        self.make_recipe(title=title, is_published=True)
        response = self.client.get(reverse('recipes:category', kwargs={'category_id': 1}))
        template_content = response.content.decode('utf-8')
        self.assertIn(title, template_content)
