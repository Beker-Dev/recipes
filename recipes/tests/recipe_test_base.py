from django.test import TestCase
from .recipe_mixin import RecipeMixin


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self) -> None:  # called before every method
        return super().setUp()

