from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User
from article.models import Article


class ArticleCreateViewTests(APITestCase):
    fixtures = ['account/test_users.yaml']

    def setUp(self):
        self.admin_user = User.objects.get(id=1)
        self.regular_user = User.objects.create_user(username='user', password='user')
        self.url = reverse('article_create')

    def test_admin_can_create_article(self):
        self.client.force_authenticate(user=self.admin_user)
        data = {'title': 'Test Article', 'content': 'This is a test article.'}

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.first().title, 'Test Article')

    def test_non_admin_cannot_create_article(self):
        self.client.force_authenticate(user=self.regular_user)
        data = {'title': 'Test Article', 'content': 'This is a test article.'}

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Article.objects.count(), 0)

    def test_unauthenticated_user_cannot_create_article(self):
        data = {'title': 'Test Article', 'content': 'This is a test article.'}

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Article.objects.count(), 0)
