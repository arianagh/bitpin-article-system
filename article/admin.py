from django.contrib import admin

from article.models import Article, FraudDetectionConfig, Score
from utilities.admin.commons import CommonModelAdmin


class ArticleAdmin(CommonModelAdmin):
    list_display = ('title', 'need_manual_review', 'created_at', 'updated_at')


class ScoreAdmin(CommonModelAdmin):
    list_display = ('article', 'user', 'value', 'is_suspicious')


class FraudDetectionConfigAdmin(CommonModelAdmin):
    list_display = ('spike_threshold', 'time_window_minutes')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(FraudDetectionConfig, FraudDetectionConfigAdmin)
