from django.contrib import admin

from article.models import Article, Score
from utilities.admin.commons import CommonModelAdmin


class ArticleAdmin(CommonModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    fields = ('title', 'content')


class ScoreAdmin(CommonModelAdmin):
    list_display = ('article', 'user', 'value')


admin.site.register(Article, ArticleAdmin)
admin.site.register(Score, ScoreAdmin)
