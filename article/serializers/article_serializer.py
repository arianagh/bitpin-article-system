from rest_framework import serializers

from article.models import Article


class ArticleWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ['title', 'content']


class ArticleReadSerializer(serializers.ModelSerializer):
    my_score = serializers.IntegerField(allow_null=True)

    class Meta:
        model = Article
        fields = ['title', 'content', 'average_rating', 'ratings_count', 'my_score']
