from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User
from article.models import Article, Score


class ArticleListViewTests(APITestCase):
    fixtures = ['account/test_users.yaml']

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.article = Article.objects.create(title="Test Article", content="Test content")
        Score.objects.create(article=self.article, user=self.user, value=4)
        self.url = reverse('article_list')

    def test_authenticated_user_can_view_article_list(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Article')
        self.assertEqual(response.data['results'][0]['my_score'], 4)

    def test_unauthenticated_user_cannot_view_article_list(self):
        response = self.client.get(self.url, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
