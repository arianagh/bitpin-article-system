from rest_framework.pagination import CursorPagination


class ArticleCursorPagination(CursorPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    ordering = '-created_at'
