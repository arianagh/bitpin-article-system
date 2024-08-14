from django.test import TestCase
from django.utils import timezone

from account.models import User
from article.helpers import ArticleRatingsAnalyzer
from article.models import Article, FraudDetectionConfig, Score


class FraudDetectionTestCase(TestCase):

    def setUp(self):
        self.config = FraudDetectionConfig.objects.create(
            time_window_minutes=10,
            spike_threshold=5,
            min_score_deviation=1,
        )
        self.article = Article.objects.create(title="Test Article", content="Test Content")
        self.now = timezone.now()
        self.analyzer = ArticleRatingsAnalyzer()

    def create_article_and_score(self, value, username):
        user = User.objects.create_user(username=f'user_{username}', email=f'email {username}',
                                        password='password')
        score = Score.objects.create(user=user, article=self.article, value=value)

        return score

    def test_all_similar(self):
        self.create_article_and_score(5, 'a')
        self.create_article_and_score(5, 'b')
        self.create_article_and_score(5, 'c')
        self.create_article_and_score(5, 'd')
        self.create_article_and_score(5, 'e')
        self.create_article_and_score(5, 'f')
        self.create_article_and_score(5, 'g')
        self.analyzer.analyze()

        suspicious_scores = Score.objects.filter(is_suspicious=True)
        self.assertEqual(suspicious_scores.count(), 7)

    def test_spike_detection_most_common(self):
        self.create_article_and_score(1, 'a')
        self.create_article_and_score(1, 'b')
        self.create_article_and_score(1, 'c')
        self.create_article_and_score(3, 'd')
        self.create_article_and_score(1, 'e')
        self.create_article_and_score(1, 'f')
        self.create_article_and_score(4, 'g')
        self.analyzer.analyze()

        suspicious_scores = Score.objects.filter(is_suspicious=True)
        self.assertEqual(suspicious_scores.count(), 5)

    def test_low_standard_deviation_detection(self):
        self.create_article_and_score(1, 'a')
        self.create_article_and_score(2, 'b')
        self.create_article_and_score(1, 'c')
        self.create_article_and_score(3, 'd')
        self.create_article_and_score(3, 'e')
        self.create_article_and_score(1, 'f')
        self.create_article_and_score(2, 'g')
        self.analyzer.analyze()

        suspicious_scores = Score.objects.filter(is_suspicious=True)
        self.assertEqual(suspicious_scores.count(), 3)

    def test_not_deviated(self):
        self.create_article_and_score(1, 'a')
        self.create_article_and_score(2, 'b')
        self.create_article_and_score(4, 'c')
        self.create_article_and_score(3, 'd')
        self.create_article_and_score(3, 'e')
        self.create_article_and_score(5, 'f')
        self.create_article_and_score(2, 'g')
        self.analyzer.analyze()

        suspicious_scores = Score.objects.filter(is_suspicious=True)
        self.assertEqual(suspicious_scores.count(), 0)

    def tearDown(self):
        Score.objects.all().delete()
        Article.objects.all().delete()
        FraudDetectionConfig.objects.all().delete()
