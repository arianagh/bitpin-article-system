from django.core.cache import cache

CACHE_KEY_ARTICLE = 'articles_to_update'

# todo
# 1- setup the celery and celery beat
# 2- check the sanity and performance of creating some ratings for an article and see it in list view # noqa
# 3- check the pagination performance and its doc in drf
# 4- we can create a script to create a 100 article
# 5- check if the updated_at of article gets changed and if so have mechanism for the ones who didn't # noqa
# changed for a day or so and have another cron job for them
# 6 neshian dadne khode user to list view


def add_article_id_to_cache(article_id):
    cache_key = CACHE_KEY_ARTICLE
    cache.add(cache_key, set())
    cache.sadd(cache_key, article_id)


def get_and_clear_article_ids_from_cache():
    cache_key = CACHE_KEY_ARTICLE
    article_ids = list(cache.smembers(CACHE_KEY_ARTICLE))
    # todo check the delete
    cache.delete(cache_key)
    return article_ids
