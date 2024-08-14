from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from article.models import Article, Score
from article.serializers.score_serializer import ScoreSerializer
from article.throttling import ArticleRateThrottle
from utilities import cache_helper


class ScoreCreateView(APIView):
    serializer_class = ScoreSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ArticleRateThrottle]

    def post(self, request, article_id):
        user = self.request.user
        article = get_object_or_404(Article, id=article_id)
        serializer = ScoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        score, created = Score.objects.update_or_create(
            article=article, user=user, defaults={'value': serializer.validated_data['value']})
        score.weight = score.calculate_weight()

        cache_helper.add_article_id_to_cache(article_id)

        return Response(serializer.data,
                        status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)
