from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User


class UserRegistrationViewTests(APITestCase):
    fixtures = ['account/test_users.yaml']

    def setUp(self):
        self.url = reverse('registration')
        self.user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'securepassword123'
        }

    def test_user_registration(self):
        response = self.client.post(self.url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username=self.user_data['username'])
        self.assertIsNotNone(user)
        self.assertEqual(user.email, self.user_data['email'])

    def test_user_registration_with_missing_field(self):
        incomplete_data = {
            'email': 'arian@example.com',
            'first_name': 'arian',
            'last_name': 'agh',
        }
        response = self.client.post(self.url, incomplete_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_registration_duplicated(self):
        data = {'username': 'arian', 'email': 'arian@gmail.com', 'password': "hello"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
