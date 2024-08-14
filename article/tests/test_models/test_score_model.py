from django.test import TestCase

from account.models import User
from article.models import Article, FraudDetectionConfig, Score


class ScoreModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='john', password='12345')
        self.config = FraudDetectionConfig.objects.create(
            time_window_minutes=10,
            spike_threshold=50,
            min_score_deviation=1,
        )

    def create_article_and_score(self, value):
        article = Article.objects.create(title=f"Test Article {value}", content="Test Content")
        score = Score.objects.create(user=self.user, article=article, value=value)
        return score

    def test_calculate_weight_low_diversity(self):
        self.create_article_and_score(1)
        self.create_article_and_score(1)
        self.create_article_and_score(2)
        self.create_article_and_score(2)
        self.create_article_and_score(1)

        article = Article.objects.create(title="Test Article 6", content="Test Content")
        score = Score.objects.create(user=self.user, article=article, value=3)
        score.calculate_weight()

        score.refresh_from_db()

        # Check if the weight is 0.7 due to low diversity in user ratings
        self.assertEqual(score.weight, 0.7)

    def test_calculate_weight_high_diversity(self):
        self.create_article_and_score(1)
        self.create_article_and_score(5)
        self.create_article_and_score(3)
        self.create_article_and_score(2)
        self.create_article_and_score(4)

        article = Article.objects.create(title="Test Article 6", content="Test Content")
        score = Score.objects.create(user=self.user, article=article, value=3)
        score.calculate_weight()

        score.refresh_from_db()

        # Check if the weight is 1.0 due to high diversity in user ratings
        self.assertEqual(score.weight, 1.0)

    def test_calculate_weight_few_scores(self):
        self.create_article_and_score(1)
        self.create_article_and_score(2)
        self.create_article_and_score(1)

        article = Article.objects.create(title="Test Article 4", content="Test Content")
        score = Score.objects.create(user=self.user, article=article, value=2)
        score.calculate_weight()

        score.refresh_from_db()

        # Check if the weight is 0.5 due to fewer than 5 scores
        self.assertEqual(score.weight, 0.5)
