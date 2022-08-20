from .base import AuthorsBaseTest
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from django.urls import reverse
import time


@pytest.mark.functional_test
class AuthorsLoginFunctionalTest(AuthorsBaseTest):
    def connect_endpoint(self, e='authors:login'):
        endpoint = reverse(e)
        self.browser.get(self.live_server_url + endpoint)

    def test_user_valid_data_can_login_successfully(self):
        password_str = 'P@ssword1234'
        user = User.objects.create_user(
            username='user.user',
            password=password_str
        )
        self.connect_endpoint()
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        self.find_element_by_placeholder(web_element=form, placeholder='Usuário').send_keys(user.username)
        self.find_element_by_placeholder(web_element=form, placeholder='Senha').send_keys(password_str)
        form.submit()
        self.assertIn('Login realizado com sucesso!', self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_login_create_raises_404_if_not_post_method(self):
        self.connect_endpoint('authors:login_create')
        self.assertIn('Not Found', self.browser.find_element(By.TAG_NAME, 'body').text)

    def test_form_login_is_invalid(self):
        self.connect_endpoint()
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        self.find_element_by_placeholder(form, 'Usuário').send_keys(' ')
        self.find_element_by_placeholder(form, 'Senha').send_keys(' ')
        form.submit()
        self.assertIn('Usuário ou Senha invalidos', self.browser.find_element(By.TAG_NAME, 'body').text)
    
    def test_form_login_invalid_credentials(self):
        self.connect_endpoint()
        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        self.find_element_by_placeholder(form, 'Usuário').send_keys('user.false')
        self.find_element_by_placeholder(form, 'Senha').send_keys('fake@1234')
        form.submit()
        self.assertIn('Usuário ou Senha invalidos', self.browser.find_element(By.TAG_NAME, 'body').text)
