from rest_framework import test
from recipes.tests.recipe_mixin import RecipeMixin
from django.urls import reverse
from unittest.mock import patch


class RecipeApiV2Test(test.APITestCase, RecipeMixin):
    def test_recipe_api_list_returns_status_code_200(self):
        response = self.client.get(reverse('recipes:api-v2-list'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_api_list_loads_correct_number_of_recipes(self):
        wanted_recipes = 2
        self.make_recipes(amount=wanted_recipes)
        response = self.client.get(reverse('recipes:api-v2-list'))
        self.assertEqual(response.data.get('count'), wanted_recipes)

    @patch('recipes.views.RecipePaginationV2.page_size', new=3)
    def test_recipe_api_list_is_paginated(self):
        self.make_recipes(amount=6)
        response = self.client.get(reverse('recipes:api-v2-list'))
        self.assertEqual(len(response.data.get('results')), 3)

    def test_recipe_api_list_does_not_show_not_published_recipes(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:api-v2-list'))
        self.assertEqual(response.data.get('count'), 0)
