from rest_framework import test
from recipes.tests.recipe_mixin import RecipeMixin
from django.urls import reverse
from unittest.mock import patch


class RecipeApiV2Test(test.APITestCase, RecipeMixin):
    def test_recipe_api_list_returns_status_code_200(self):
        response = self.client.get(reverse('recipes:api-v1-list'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        wanted_recipes = 2
        self.make_recipes(amount=wanted_recipes)
        response = self.client.get(reverse('recipes:api-v1-list'))
        self.assertEqual(response.data.get('count'), wanted_recipes)

    @patch('recipes.views.RecipePaginationV1.page_size', new=3)
    def test_recipe_api_list_is_paginated(self):
        self.make_recipes(amount=6)
        response = self.client.get(reverse('recipes:api-v1-list'))
        self.assertEqual(len(response.data.get('results')), 3)

    def test_recipe_api_list_does_not_show_not_published_recipes(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:api-v1-list'))
        self.assertEqual(response.data.get('count'), 0)

    def test_recipe_api_list_returns_recipes_with_correct_category_filter(self):
        user = self.make_author(username='Us3r', password='asdf123')
        category1 = self.make_category(name='Junk-Food')
        category2 = self.make_category(name='Healthy-Food')
        self.make_recipe(title='recipe1', category=category1, author=user, is_published=True)
        self.make_recipe(title='recipe2', category=category1, author=user, is_published=True)
        self.make_recipe(title='recipe3', category=category2, author=user, is_published=True)
        url = reverse('recipes:api-v1-list') + '?category=' + category1.name
        response = self.client.get(url)
        self.assertEqual(response.data.get('count'), 2)

    def test_recipe_api_list_returns_recipes_with_correct_author_filter(self):
        user = self.make_author(username='Us3r', password='asdf123')
        user2 = self.make_author(username='Us3r2', password='asdf123')
        category1 = self.make_category(name='Junk-Food')
        self.make_recipe(title='recipe1', category=category1, author=user, is_published=True)
        self.make_recipe(title='recipe2', category=category1, author=user, is_published=True)
        self.make_recipe(title='recipe3', category=category1, author=user2, is_published=True)
        url = reverse('recipes:api-v1-list') + '?author=' + user.username
        response = self.client.get(url)
        self.assertEqual(response.data.get('count'), 2)

