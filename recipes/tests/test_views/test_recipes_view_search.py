from recipes.tests.recipe_test_base import RecipeTestBase
from django.urls import reverse, resolve
from recipes import views


class TestRecipesViewsSearch(RecipeTestBase):
    def test_recipes_search_view_function_is_correct(self):
        view = resolve(reverse('recipes:search'))
        self.assertIs(view.func, views.search)

    def test_recipes_search_view_function_returns_status_code_200_ok(self):
        url = reverse('recipes:search') + '?q=test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_recipes_search_view_function_loads_correct_template(self):
        url = reverse('recipes:search') + '?q=test'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_view_function_raises_404_if_not_search_term(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_view_function_search_term_is_on_page_title_and_escaped(self):
        url = reverse('recipes:search') + '?q=TestSearch'
        response = self.client.get(url)
        template_content = response.content.decode('utf-8')
        self.assertIn('Search for "TestSearch"', template_content)

    def test_recipe_search_view_function_search_can_find_recipe_by_title(self):

        title1 = 'New Recipe 1'
        title2 = 'New Recipe 2'

        recipe1 = self.make_recipe(title=title1, slug='xyz-1', author=self.make_author(username='user1'))
        recipe2 = self.make_recipe(title=title2, slug='xyz-2', author=self.make_author(username='user2'))

        url1 = reverse('recipes:search') + f'?q={title1}'
        url2 = reverse('recipes:search') + f'?q={title2}'

        response1 = self.client.get(url1)
        response2 = self.client.get(url2)

        context1 = response1.context.get('recipes')
        context2 = response2.context.get('recipes')

        self.assertIn(recipe1, context1)
        self.assertIn(recipe2, context2)
