from unittest.mock import patch
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Não há receitas publicadas!', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_search_recipe_by_input(self):
        recipes = self.make_recipes()
        title_needed = recipes[0].title
        self.browser.get(self.live_server_url)
        search_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Buscar receita"]')
        search_input.send_keys(title_needed, Keys.ENTER)
        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text
        )

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipes(10)
        self.browser.get(self.live_server_url)
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()
        self.assertEqual(len(self.browser.find_elements(By.CLASS_NAME, 'recipe')), 2)
