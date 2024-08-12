import logging

from django.core.cache import cache

CACHE_KEY_ARTICLE = 'articles_to_update'


def add_article_id_to_cache(article_id):
    try:
        cache_key = CACHE_KEY_ARTICLE
        redis_client = cache.client.get_client()
        redis_client.sadd(cache_key, article_id)
    except Exception as e:
        logging.error(f"Failed to add article ID {article_id} to cache: {e}")


def get_and_clear_article_ids_from_cache():
    try:
        cache_key = CACHE_KEY_ARTICLE
        redis_client = cache.client.get_client()
        article_ids = redis_client.smembers(CACHE_KEY_ARTICLE)
        redis_client.delete(cache_key)
        return article_ids
    except Exception as e:
        logging.error(f"Failed to get and clear article IDs from cache: {e}")
        return set()
