from celery import shared_task

from article.models import Article
from utilities import cache_helper


@shared_task
def batch_update_article_ratings():
    article_ids = cache_helper.get_and_clear_article_ids_from_cache()

    if article_ids:
        Article.bulk_update_articles(article_ids)


@shared_task
def update_stale_articles():
    Article.bulk_update_stale_articles()
