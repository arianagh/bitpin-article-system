from rest_framework import serializers

from article.models import Score


class ScoreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Score
        fields = ['value']
