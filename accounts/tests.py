from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase

from accounts.forms import RegisterForm


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.url = reverse("accounts:register")

    def test_register_view_get(self):
        request = self.client.get(self.url)
        self.assertEqual(request.status_code, 200)
        self.assertIsInstance(request.context_data['form'], RegisterForm)

    def test_register_view_post(self):
        data = {
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'password1': 'testpassword2',
            'password2': 'testpassword2',
        }
        request = self.client.post(self.url, data)
        self.assertEqual(request.status_code, 302)
        self.assertEqual(get_user_model().objects.filter(username='testuser2').count(), 1)
        self.assertTrue(self.client.login(username='testuser2', password='testpassword2'))
