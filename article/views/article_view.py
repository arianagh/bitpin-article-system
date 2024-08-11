from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from article.models import Article
from article.serializers.article_serializer import ArticleReadSerializer, ArticleWriteSerializer


class ArticleCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ArticleWriteSerializer


class ArticleListView(APIView):

    def get(self, request):
        queryset = Article.objects.all()
        # Instantiate the paginator
        # paginator = PostCursorPagination()
        # paginated_queryset = paginator.paginate_queryset(queryset, request)
        #
        # if paginated_queryset is None:
        #     raise NotFound("No more pages")

        # Serialize the paginated data
        serializer = ArticleReadSerializer(queryset, many=True)
        return Response(serializer.data)

        # Return paginated response
        # return paginator.get_paginated_response(serializer.data)
