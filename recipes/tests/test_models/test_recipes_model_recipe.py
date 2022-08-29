from django.core.exceptions import ValidationError
from recipes.tests.recipe_test_base import RecipeTestBase
from recipes.models import Recipe
from parameterized import parameterized


class TestRecipesModelRecipe(RecipeTestBase):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()

    @parameterized.expand([
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65)
        ])
    def test_recipe_fields_max_length(self, field, max_length):
        setattr(self.recipe, field, 'a' * (max_length + 1))
        with self.assertRaises(ValidationError) as e:
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_is_false_by_default(self):
        self.assertFalse(
            self.recipe.preparation_steps_is_html,
            msg='recipe.preparation_steps_is_html must be false as default'
        )

    def test_recipe_is_published_is_false_by_default(self):
        self.assertFalse(
            self.recipe.is_published,
            msg='recipe.is_published must be false as default'
        )

    def test_recipe_str_method_returns_recipe_title(self):
        title = 'newRecipe testing'
        self.recipe.title = title
        self.assertEqual(str(self.recipe), title)
