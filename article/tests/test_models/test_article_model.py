from django.test import TestCase
from django.utils import timezone

from account.models import User
from article.models import Article, Score


class ArticleModelTests(TestCase):
    fixtures = ['account/test_users.yaml']

    def setUp(self):
        self.user = User.objects.get(id=1)
        self.second_user = User.objects.create_user(username='admin', password='admin')
        self.article1 = Article.objects.create(title="Article 1", content="Content 1")
        self.article2 = Article.objects.create(title="Article 2", content="Content 2")

        Score.objects.create(article=self.article1, user=self.user, value=3, weight=1)
        Score.objects.create(article=self.article1, user=self.second_user, value=5, weight=1)
        Score.objects.create(article=self.article2, user=self.user, value=3, weight=1,
                             is_suspicious=True)

    def test_bulk_update_articles(self):
        Article.bulk_update_articles([self.article1.id, self.article2.id])

        self.article1.refresh_from_db()
        self.article2.refresh_from_db()

        self.assertEqual(self.article1.average_rating, 4.0)
        self.assertEqual(self.article1.ratings_count, 2)
        self.assertEqual(self.article2.average_rating, 0.0)
        self.assertEqual(self.article2.ratings_count, 0)

    def test_bulk_update_stale_articles(self):
        stale_date = timezone.now() - timezone.timedelta(days=3)
        Article.objects.filter(id__in=[self.article1.id]).update(updated_at=stale_date)

        Article.bulk_update_stale_articles()

        self.article1.refresh_from_db()
        self.assertAlmostEqual(self.article1.updated_at, timezone.now(),
                               delta=timezone.timedelta(seconds=30))

    def test_bulk_flag_suspicious_articles(self):
        Article.bulk_flag_suspicious_articles()

        self.article1.refresh_from_db()
        self.article2.refresh_from_db()

        self.assertFalse(self.article1.need_manual_review)
        self.assertTrue(self.article2.need_manual_review)

        self.assertAlmostEqual(self.article2.updated_at, timezone.now(),
                               delta=timezone.timedelta(seconds=30))
