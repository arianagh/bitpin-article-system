import logging

from celery import shared_task

from article.helpers import ArticleRatingsAnalyzer
from article.models import Article
from utilities import cache_helper


@shared_task
def batch_update_article_ratings():
    logging.info('Batch updating the article ratings')

    article_ids = cache_helper.get_and_clear_article_ids_from_cache()

    if article_ids:
        Article.bulk_update_articles(article_ids)


@shared_task
def update_stale_articles():
    logging.info('Updating the stale articles')

    Article.bulk_update_stale_articles()


@shared_task
def flag_suspicious_articles():
    logging.info('Updating the articles which have suspicious ratings')

    Article.bulk_flag_suspicious_articles()


@shared_task
def find_suspicious_ratings():
    logging.info('Find the ratings which are suspicious')

    analyzer = ArticleRatingsAnalyzer()
    analyzer.analyze()
