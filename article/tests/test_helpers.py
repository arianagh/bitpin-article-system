from django.test import TestCase
from faker import Faker

from account.models import User
from article.helpers import ArticleRatingsAnalyzer
from article.models import Article, FraudDetectionConfig, Score

fake = Faker()


class FraudDetectionTestCase(TestCase):

    def setUp(self):
        self.config = FraudDetectionConfig.objects.create(
            time_window_minutes=10,
            spike_threshold=5,
            min_score_deviation=1,
        )
        self.article = Article.objects.create(title="Test Article", content="Test Content")
        self.analyzer = ArticleRatingsAnalyzer()

    def create_scores(self, scores):
        return [self.create_article_and_score(value) for value in scores]

    def create_article_and_score(self, value):
        username = fake.user_name()
        user = User.objects.create_user(username=f'user_{username}', email=f'email {username}',
                                        password='password')
        score = Score.objects.create(user=user, article=self.article, value=value)
        return score

    def analyze_and_assert(self, expected_suspicious_count, expected_suspicious_ids=None):
        self.analyzer.analyze()
        suspicious_scores = Score.objects.filter(is_suspicious=True)
        self.assertEqual(suspicious_scores.count(), expected_suspicious_count)
        actual_suspicious_ids = list(suspicious_scores.order_by('id').values_list('id', flat=True))
        self.assertEqual(actual_suspicious_ids, expected_suspicious_ids)

    def test_all_similar(self):
        scores = [5, 5, 5, 5, 5, 5, 5]
        created_scores = self.create_scores(scores)
        expected_suspicious_ids = [score.id for score in created_scores]
        self.analyze_and_assert(expected_suspicious_count=7,
                                expected_suspicious_ids=expected_suspicious_ids)

    def test_spike_detection_most_common(self):
        scores = [1, 1, 1, 3, 1, 1, 4]
        created_scores = self.create_scores(scores)
        expected_suspicious_ids = [created_scores[i].id for i in [0, 1, 2, 4, 5]]
        self.analyze_and_assert(expected_suspicious_count=5,
                                expected_suspicious_ids=expected_suspicious_ids)

    def test_low_standard_deviation_detection(self):
        scores = [1, 2, 1, 3, 3, 1, 2]
        created_scores = self.create_scores(scores)
        expected_suspicious_ids = [created_scores[i].id for i in [0, 2, 5]]
        self.analyze_and_assert(expected_suspicious_count=3,
                                expected_suspicious_ids=expected_suspicious_ids)

    def test_not_deviated(self):
        scores = [1, 2, 4, 3, 3, 5, 2]
        self.create_scores(scores)
        self.analyze_and_assert(expected_suspicious_count=0, expected_suspicious_ids=[])
