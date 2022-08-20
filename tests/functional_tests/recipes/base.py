from django.test import LiveServerTestCase  # run server without staticfiles
from django.contrib.staticfiles.testing import StaticLiveServerTestCase  # run server with staticfiles
from utils.browser import make_chrome_browser
from recipes.tests.recipe_mixin import RecipeMixin


class RecipeBaseFunctionalTest(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self):
        self.browser = make_chrome_browser('--headless')
        return super().setUp()

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()
