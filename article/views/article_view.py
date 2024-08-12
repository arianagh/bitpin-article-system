from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView

from article.models import Article
from article.pagination import ArticleCursorPagination
from article.serializers.article_serializer import ArticleReadSerializer, ArticleWriteSerializer


class ArticleCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ArticleWriteSerializer


class ArticleListView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = ArticleCursorPagination
    serializer_class = ArticleReadSerializer

    def get(self, request):
        user = self.request.user
        queryset = Article.objects.with_user_score(user.id).latest()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)

        serializer = ArticleReadSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
