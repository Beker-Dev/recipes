from django.test import TestCase
from authors.forms.register_form import RegisterForm
from parameterized import parameterized
from django.urls import reverse, resolve
from django.core.exceptions import ValidationError
from utils.django_forms import is_strong_password


class TestAuthorRegisterForm(TestCase):

    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@example.com',
            'password': 'Us3r.example',
            'confirm_password': 'Us3r.example'
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('first_name', 'Nome'),
        ('last_name', 'Sobrenome'),
        ('username', 'Usuário'),
        ('email', 'email@example.com'),
        ('password', 'Senha'),
        ('confirm_password', 'Confirmar Senha')
    ])
    def test_placeholder_fields_are_correct(self, form_field, form_placeholder):
        form = RegisterForm()
        placeholder = form[form_field].field.widget.attrs.get('placeholder')
        self.assertEqual(placeholder, form_placeholder)

    @parameterized.expand([
        ('first_name', ''),
        ('last_name', ''),
        (
            'username',
            'Deve conter no mínimo 4 caracteres e no máximo 150 caracteres. Sendo, letras, números e @/./+/-/_ apenas.'
        ),
        ('email', 'Email deve ser válido'),
        ('password', 'Deve conter pelo menos oito caracteres, sendo um maiúsculo, um minusculo e um número'),
        ('confirm_password', '')
    ])
    def test_help_text_fields_are_correct(self, form_field, form_help_text):
        form = RegisterForm()
        help_text = form[form_field].help_text
        self.assertEqual(help_text, form_help_text)

    @parameterized.expand([
        ('first_name', 'Nome'),
        ('last_name', 'Sobrenome'),
        ('username', 'Usuário'),
        ('email', 'Email'),
        ('password', 'Senha'),
        ('confirm_password', 'Confirmar Senha')
    ])
    def test_label_fields_are_correct(self, form_field, form_placeholder):
        form = RegisterForm()
        placeholder = form[form_field].label
        self.assertEqual(placeholder, form_placeholder)

    @parameterized.expand([
        ('username', 'Campo Usuário não pode ficar vazio'),
        ('first_name', 'Campo Nome não pode ficar vazio'),
        ('last_name', 'Campo Sobrenome não pode ficar vazio'),
        ('password', 'Campo Senha não pode ficar vazio'),
        ('confirm_password', 'Senhas não conferem')
    ])
    def test_fields_cannot_be_empty(self, field, value):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        error = response.context['form'].errors.get(field)
        self.assertIn(value, error)

    def test_username_field_min_length_must_be_4(self):
        self.form_data['username'] = 'a'*3
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        error = response.context['form'].errors.get('username')
        self.assertIn('Esse campo deve conter no mínimo 4 caracteres', error)

    def test_username_field_max_length_must_be_150(self):
        self.form_data['username'] = 'a'*151
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        error = response.context['form'].errors.get('username')
        self.assertIn('Esse campo deve conter no máximo 150 caracteres', error)

    def test_password_field_has_lower_upper_case_letters_and_numbers_and_at_least_8_characters(self):
        self.form_data['password'] = 'aasdf2Xx'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        error = response.context['form'].errors.get('password')
        self.assertNotIn('Deve conter pelo menos oito caracteres, sendo um maiúsculo, um minusculo e um número', error)

    def test_password_and_confirm_password_are_equal(self):
        self.form_data['password'] = 'asdf2Xyz'
        self.form_data['confirm_password'] = 'asdf2Xyz@'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        password_error = response.context['form'].errors.get('password')
        confirm_password_error = response.context['form'].errors.get('confirm_password')
        self.assertIn("Senhas não conferem", password_error)
        self.assertIn("Senhas não conferem", confirm_password_error)

    def test_create_author_raises_404(self):
        url = reverse('authors:register_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_form_is_valid(self):
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'Usuário registrado com sucesso!'
        template_content = response.content.decode('utf-8')
        self.assertIn(msg, template_content)

    def test_email_field_must_be_unique(self):
        url = reverse('authors:register_create')
        self.form_data['email'] = 'new_user@hotmail.com'
        self.client.post(url, data=self.form_data, follow=True)
        # --------------- created once ----------------
        response = self.client.post(url, data=self.form_data, follow=True)
        error = response.context['form'].errors.get('email')
        self.assertIn('Email já está sendo utilizado, por favor informe outro email', error)

    def test_created_author_can_login(self):
        url = reverse('authors:register_create')
        self.form_data.update({
            'username': 'Us3r',
            'password': 'asdfF2.COM23',
            'confirm_password': 'asdfF2.COM23'
        })
        self.client.post(url, data=self.form_data, follow=True)
        is_authenticated = self.client.login(
            username=self.form_data.get('username'),
            password=self.form_data.get('password')
        )
        self.assertTrue(is_authenticated)
