from django.contrib import admin

from article.models import Article, FraudDetectionConfig, Score
from utilities.admin.commons import CommonModelAdmin


class ArticleAdmin(CommonModelAdmin):
    list_display = ('title', 'need_manual_review', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('need_manual_review', )


class ScoreAdmin(CommonModelAdmin):
    list_display = ('article', 'user', 'value', 'is_suspicious')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_suspicious', )


class FraudDetectionConfigAdmin(CommonModelAdmin):
    list_display = ('spike_threshold', 'time_window_minutes')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(FraudDetectionConfig, FraudDetectionConfigAdmin)
