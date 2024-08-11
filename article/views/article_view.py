from django.db.models import Avg, Count
from rest_framework import generics
# from rest_framework.exceptions import NotFound
from rest_framework.pagination import CursorPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from article.models import Article
from article.serializers.article_serializer import ArticleReadSerializer, ArticleWriteSerializer


class ArticleCursorPagination(CursorPagination):
    page_size = 5
    ordering = '-id'


class ArticleCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ArticleWriteSerializer


class ArticleListView(APIView):

    def get(self, request):
        # queryset = Article.objects.prefetch_related('ratings').all()
        # # Instantiate the paginator
        # paginator = ArticleCursorPagination()
        # paginated_queryset = paginator.paginate_queryset(queryset, request)
        #
        # if paginated_queryset is None:
        #     raise NotFound("No more pages")
        #
        # serializer = ArticleReadSerializer(paginated_queryset, many=True)
        # return paginator.get_paginated_response(serializer.data)
        queryset = Article.objects.annotate(a=Avg('ratings__value'), b=Count('ratings__id'))
        for article in queryset:
            article.average_rating = article.a or 0.0
            article.ratings_count = article.b or 0
        serializer = ArticleReadSerializer(queryset, many=True)
        return Response(serializer.data)
