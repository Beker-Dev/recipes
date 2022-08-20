from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from django.urls import reverse


@pytest.mark.functional_test
class AuthorsRegisterFunctionalTest(AuthorsBaseTest):

    def fill_form_with_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')
        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def get_form(self):
        form_xpath = '/html/body/main/div[2]/form'
        return self.browser.find_element(By.XPATH, form_xpath)

    def connect_endpoint(self):
        endpoint = reverse('authors:register')
        self.browser.get(self.live_server_url + endpoint)

    def form_field_test_with_callback(self, callback):
        self.connect_endpoint()
        form = self.get_form()
        self.fill_form_with_dummy_data(form)
        #form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        callback(form)
        return form

    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.find_element_by_placeholder(form, 'Nome')
            first_name_field.send_keys(' ', Keys.ENTER)
            form = self.get_form()
            self.assertIn('Campo Nome não pode ficar vazio', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.find_element_by_placeholder(form, 'Sobrenome')
            last_name_field.send_keys(' ', Keys.ENTER)
            form = self.get_form()
            self.assertIn('Campo Sobrenome não pode ficar vazio', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_username_error_message(self):
        def callback(form):
            username_field = self.find_element_by_placeholder(form, 'Usuário')
            username_field.send_keys(' ', Keys.ENTER)
            form = self.get_form()
            self.assertIn('Campo Usuário não pode ficar vazio', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_email_error_message(self):
        def callback(form):
            email_field = self.find_element_by_placeholder(form, 'email@example.com')
            email_field.send_keys(' ', Keys.ENTER)
            form = self.get_form()
            self.assertIn('Campo Email não pode ficar vazio', form.text)
        self.form_field_test_with_callback(callback)

    def test_empty_password_error_message(self):
        def callback(form):
            password_field = self.find_element_by_placeholder(form, 'Senha')
            password_field.send_keys(' ', Keys.ENTER)
            form = self.get_form()
            self.assertIn('Campo Senha não pode ficar vazio', form.text)
        self.form_field_test_with_callback(callback)

    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.find_element_by_placeholder(form, 'email@example.com')
            email_field.send_keys('invalid@email', Keys.ENTER)
            form = self.get_form()
            self.assertIn('Informe um endereço de email válido', form.text)
        self.form_field_test_with_callback(callback)

    def test_password_do_not_match(self):
        def callback(form):
            password_field = self.find_element_by_placeholder(form, 'Senha')
            password_field.send_keys('Asdf1234')
            confirm_password_field = self.find_element_by_placeholder(form, 'Confirmar Senha')
            confirm_password_field.send_keys('Asdf4321', Keys.ENTER)
            form = self.get_form()
            self.assertIn('Senhas não conferem', form.text)

        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_successfully(self):
        self.connect_endpoint()
        form = self.get_form()
        fields = (
            ('Nome', 'Joao'),
            ('Sobrenome', 'Silva'),
            ('Usuário', 'joao.silva'),
            ('email@example.com', 'joao.s@email.com'),
            ('Senha', 'P@550wRd'),
            ('Confirmar Senha', 'P@550wRd'),
        )
        for field in fields:
            self.find_element_by_placeholder(form, field[0]).send_keys(field[1])
        else:
            form.submit()
            form = self.browser.find_element(By.TAG_NAME, 'body')
            self.assertIn('Usuário registrado com sucesso!', form.text)
