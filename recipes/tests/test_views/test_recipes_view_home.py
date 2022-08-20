from recipes.tests.recipe_test_base import RecipeTestBase
from django.urls import reverse, resolve
from recipes import views
from unittest.mock import patch


class TestRecipesViewsHome(RecipeTestBase):
    def test_recipes_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipes_home_view_function_returns_status_code_200_ok(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipes_home_view_function_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipes_home_view_template_shows_no_recipes_found_if_no_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        template_content = response.content.decode('utf-8')
        text = 'Não há receitas publicadas!'
        self.assertIn(text, template_content)
        #  self.fail('I have to write more code')  -- this will fail code

    def test_recipes_home_view_template_shows_recipes_if_recipes(self):
        title = 'New Recipe'
        self.make_recipe(title=title)
        response = self.client.get(reverse('recipes:home'))
        template_content = response.content.decode('utf-8')
        self.assertIn(title, template_content)

    def test_recipes_home_view_template_does_not_load_recipe_if_not_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        template_content = response.content.decode('utf-8')
        text = 'Não há receitas publicadas!'
        self.assertIn(text, template_content)

    @patch('recipes.views.PER_PAGE', new=3)  # alter object value and return old value again, after it's used
    def test_recipes_home_view_function_is_paginated(self):
        self.make_recipes(amount=9)

        # with patch('recipes.views.PER_PAGE', new=6):  #other way for using patch
            # code here

        url = reverse('recipes:home') + '?page=1'
        response = self.client.get(url)
        recipes = response.context.get('recipes')
        paginator = recipes.paginator
        self.assertEqual(paginator.num_pages, 3)
        self.assertEqual(len(paginator.get_page(1)), 3)
        self.assertEqual(paginator.count, 9)

