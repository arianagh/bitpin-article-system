from datetime import timedelta

import numpy as np
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from article.queryset import ArticleQueryset
from utilities.models.base_model import BaseModel


class Article(BaseModel):
    title = models.CharField(max_length=100, verbose_name='نام مطلب', db_index=True)
    content = models.TextField(verbose_name='محتوای مطلب')
    average_rating = models.FloatField(default=0.0, blank=True, verbose_name='میانگین امتیازها')
    ratings_count = models.PositiveIntegerField(default=0, blank=True,
                                                verbose_name='تعداد امتیازها')
    need_manual_review = models.BooleanField(default=False)

    objects = ArticleQueryset.as_manager()

    @classmethod
    def bulk_update_articles(cls, article_ids):
        """ Fetch articles and perform a bulk update on their ratings. """

        articles = cls.objects.get_articles_for_update(article_ids).with_ratings_data()
        updated_articles = []
        for article in articles:
            article.average_rating = article.avg_rating
            article.ratings_count = article.rate_count
            article.updated_at = timezone.now()
            updated_articles.append(article)

        cls.objects.bulk_update(updated_articles,
                                ['average_rating', 'ratings_count', 'updated_at'], batch_size=750)

    @classmethod
    def bulk_update_stale_articles(cls):
        """ Update articles that haven't been updated in more than N days. """

        threshold_date = timezone.now() - timedelta(days=2)

        stale_articles = cls.objects.filter(updated_at__lt=threshold_date)
        article_ids = stale_articles.values_list('id', flat=True)

        if article_ids:
            cls.bulk_update_articles(article_ids)

    @classmethod
    def bulk_flag_suspicious_articles(cls):
        """ Update the articles that had suspiciously flagged scores for review. """

        articles = cls.objects.with_suspicious_ratings()
        updated_articles = []
        for article in articles:
            article.need_manual_review = article.need_review
            article.updated_at = timezone.now()
            updated_articles.append(article)

        cls.objects.bulk_update(updated_articles, ['need_manual_review', 'updated_at'],
                                batch_size=750)

    def __str__(self):
        return self.title


class Score(BaseModel):
    article = models.ForeignKey(Article, related_name='ratings', on_delete=models.CASCADE,
                                verbose_name='مطلب')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=0,
                                     validators=[MinValueValidator(0),
                                                 MaxValueValidator(5),
                                                 ], db_index=True, verbose_name='مقدار امتیاز')
    weight = models.FloatField(default=1.0)
    is_suspicious = models.BooleanField(default=False)
    reason_of_suspicion = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('article', 'user')

    def calculate_weight(self):
        """
        Calculate the weight of this score based on certain factors.
        """
        fraud_config = FraudDetectionConfig.objects.first()
        user_scores = Score.objects.filter(user=self.user)
        score_count = user_scores.count()

        if score_count < 5:
            self.weight = 0.5
        elif np.std([score.value for score in user_scores]) < fraud_config.min_score_deviation:
            self.weight = 0.7
        else:
            self.weight = 1.0

        self.save(update_fields=['weight'])


class FraudDetectionConfig(models.Model):
    spike_threshold = models.IntegerField(
        default=2000, help_text="Max number of ratings in the time window before flagging.")
    time_window_minutes = models.IntegerField(
        default=10, help_text="Time window in minutes to analyze for spikes.")
    min_score_deviation = models.FloatField(
        default=1.0, help_text="Minimum standard deviation of scores to avoid flagging.")
