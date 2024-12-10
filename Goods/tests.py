from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class TestIndex(TestCase):

    def test_index(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

class LoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_successful_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertRedirects(response, reverse('index'))

    def test_unsuccessful_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser321',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)

