from django.db import models
from django.db.models import BooleanField, Count, ExpressionWrapper, F, FloatField, OuterRef, Q, \
    Subquery, Sum
from django.db.models.functions import Coalesce


class ArticleQueryset(models.QuerySet):

    def with_ratings_data(self):
        return self.annotate(
            weighted_sum=Coalesce(
                Sum(F('ratings__value') * F('ratings__weight')), 0.0, output_field=FloatField()),
            total_weight=Coalesce(Sum(F('ratings__weight')), 1.0, output_field=FloatField()),
            rate_count=Coalesce(Count('ratings__id'), 0)).annotate(
                avg_rating=Coalesce(
                    F('weighted_sum') / F('total_weight'), 0.0, output_field=FloatField()))

    def with_suspicious_ratings(self):
        return self.annotate(
            need_review=ExpressionWrapper(
                Q(ratings__is_suspicious=True), output_field=BooleanField()))

    def get_articles_for_update(self, article_ids):
        return self.filter(id__in=article_ids, ratings__is_suspicious=False)

    def latest_by_time(self):
        return self.order_by('-created_at')

    def with_user_score(self, user_id):
        from article.models import Score

        return self.annotate(
            my_score=Subquery(
                Score.objects.filter(article=OuterRef('pk'), user_id=user_id).values('value')[:1]))
