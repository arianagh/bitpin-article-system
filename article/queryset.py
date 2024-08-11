from django.db import models
from django.db.models import Avg, Count


class ArticleQueryset(models.QuerySet):

    def with_ratings_data(self):
        return self.annotate(avg_rate=Avg('ratings__value'), rate_count=Count('ratings__id'))

    def get_articles_for_update(self, article_ids):
        return self.filter(id__in=article_ids)
