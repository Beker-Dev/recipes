from recipes.tests.recipe_test_base import RecipeTestBase
from django.core.exceptions import ValidationError
from recipes.models import Category


class TestRecipesModelCategory(RecipeTestBase):
    def setUp(self):
        self.category = self.make_category()
        super().setUp()

    def test_recipe_category_name_max_length(self):
        max_length = 65
        self.category.name = 'a' * (max_length + 1)

        with self.assertRaises(ValidationError) as e:
            self.category.full_clean()
            self.category.save()

    def test_recipe_category_str_method_returns_recipe_title(self):
        self.category.name = 'Other Category'
        self.assertEqual(str(self.category), self.category.name)
