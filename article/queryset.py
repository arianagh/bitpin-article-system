from django.db import models
from django.db.models import Avg, Count, OuterRef, Subquery
from django.db.models.functions import Coalesce


class ArticleQueryset(models.QuerySet):

    def with_ratings_data(self):
        return self.annotate(
            avg_rating=Coalesce(Avg('ratings__value'), 0.0),
            rate_count=Coalesce(Count('ratings__id'), 0))

    def get_articles_for_update(self, article_ids):
        return self.filter(id__in=article_ids)

    def latest(self):
        return self.order_by('-created_at')

    def with_user_score(self, user_id):
        from article.models import Score

        return self.annotate(
            my_score=Subquery(
                Score.objects.filter(article=OuterRef('pk'), user_id=user_id).values('value')[:1]))
