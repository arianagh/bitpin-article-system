from django.urls import path

from article.views.article_view import ArticleCreateView, ArticleListView
from article.views.score_view import ScoreCreateView

urlpatterns = [
    path('create/', ArticleCreateView.as_view(), name='article_create'),
    path('list/', ArticleListView.as_view(), name='article_list'),
    path('score/<int:article_id>/create/', ScoreCreateView.as_view(), name='score_create'),
]
