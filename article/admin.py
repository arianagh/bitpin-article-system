from django.contrib import admin

from article.models import Article
from utilities.admin.commons import CommonModelAdmin


class ArticleAdmin(CommonModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    fields = ('title', 'content')


admin.site.register(Article, ArticleAdmin)
