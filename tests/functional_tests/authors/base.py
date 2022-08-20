from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
from selenium.webdriver.common.by import By


class AuthorsBaseTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = make_chrome_browser('--headless')
        return super().setUp()

    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

    def find_element_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(By.XPATH, f'//input[@placeholder="{placeholder}"]')
