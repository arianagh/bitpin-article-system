from datetime import timedelta

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

    objects = ArticleQueryset.as_manager()

    @classmethod
    def bulk_update_articles(cls, article_ids):
        """Fetch articles and perform a bulk update on their ratings."""

        articles = cls.objects.get_articles_for_update(article_ids).with_ratings_data()
        updated_articles = []

        for article in articles:
            article.average_rating = article.avg_rate
            article.ratings_count = article.rate_count
            article.updated_at = timezone.now()
            updated_articles.append(article)

        cls.objects.bulk_update(updated_articles,
                                ['average_rating', 'ratings_count', 'updated_at'])

    @classmethod
    def bulk_update_stale_articles(cls):
        """Update articles that haven't been updated in more than N days."""

        threshold_date = timezone.now() - timedelta(days=2)

        stale_articles = cls.objects.filter(updated_at__lt=threshold_date)
        article_ids = stale_articles.values_list('id', flat=True)

        if article_ids:
            cls.bulk_update_articles(article_ids)

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

    class Meta:
        unique_together = ('article', 'user')
