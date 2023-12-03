from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from user.forms import RegisterForm


class UserViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_view(self):
        """Тестирование представления домашней страницы."""
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'user/home.html')

    def test_sign_up_get(self):
        """Тестирование представления регистрации с запросом GET."""
        url = reverse('sign_up')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], RegisterForm)
        self.assertTemplateUsed(response, 'registration/sign_up.html')

    def test_sign_up_post_valid(self):
        """Тестирование представления регистрации с запросом POST и валидными данными."""
        url = reverse('sign_up')
        data = {
            'username': 'newuser',
            'email': 'testemail@gmail.com',
            'password1': 'complexpassword',
            'password2': 'complexpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_sign_up_post_invalid(self):
        """Тестирование представления регистрации с запросом POST и невалидными данными."""
        url = reverse('sign_up')
        data = {
            'username': 'newuser',
            'password1': 'complexpassword',
            'password2': 'wrongpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='newuser').exists())
