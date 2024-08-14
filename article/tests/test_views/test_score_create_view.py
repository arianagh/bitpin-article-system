from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from account.models import User
from article.models import Article, Score


class ScoreCreateViewTests(APITestCase):
    fixtures = ['article/test_score_create.yaml']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.article = Article.objects.get(pk=1)
        self.url = reverse('score_create', kwargs={'article_id': self.article.id})
        self.second_user = User.objects.create_user(username='admin', password='admin')

    def test_create_score(self):
        self.client.force_authenticate(user=self.second_user)
        data = {'value': 4}

        with patch('utilities.cache_helper.add_article_id_to_cache') as mock_cache:
            response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Score.objects.count(), 2)
        self.assertEqual(Score.objects.last().value, 4)
        self.assertEqual(Score.objects.last().weight, 0.5)
        mock_cache.assert_called_once_with(self.article.id)

    def test_update_score(self):
        self.client.force_authenticate(user=self.user)
        data = {'value': 5}

        with patch('utilities.cache_helper.add_article_id_to_cache') as mock_cache:
            response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Score.objects.count(), 1)
        self.assertEqual(Score.objects.first().value, 5)
        self.assertEqual(Score.objects.first().weight, 0.5)
        mock_cache.assert_called_once_with(self.article.id)

    def test_invalid_score(self):
        self.client.force_authenticate(user=self.user)

        data = {'value': 6}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_request(self):
        data = {'value': 4}
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
