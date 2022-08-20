from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestAuthorLogout(TestCase):
    def create_user_and_login(self):
        pw_str = 'P@ssw0rd'
        user = User.objects.create_user(username='user.user', password=pw_str)
        self.client.login(username=user.username, password=pw_str)
        return user.username, pw_str

    def get_url(self):
        return reverse('authors:logout')

    def test_user_tries_to_logout_using_get_method_and_raises_404(self):
        self.create_user_and_login()
        url = self.get_url()
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 404)

    def test_user_tries_to_logout_another_user_and_raises_403(self):
        self.create_user_and_login()
        url = self.get_url()
        response = self.client.post(url, data={'username': 'other_user'}, follow=True)
        self.assertEqual(response.status_code, 403)

    def test_user_tries_to_logout_another_user_and_return_200(self):
        username, _ = self.create_user_and_login()
        url = self.get_url()
        response = self.client.post(url, data={'username': username}, follow=True)
        self.assertEqual(response.status_code, 200)

