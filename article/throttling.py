from rest_framework.throttling import SimpleRateThrottle


class ArticleRateThrottle(SimpleRateThrottle):
    scope = 'score'

    def get_cache_key(self, request, view):
        article_id = view.kwargs.get('article_id')
        if not article_id:
            return None

        return f'throttle_{self.scope}_{article_id}'
