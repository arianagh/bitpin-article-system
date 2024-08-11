from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from utilities.models.base_model import BaseModel


class Article(BaseModel):
    title = models.CharField(max_length=100, verbose_name='نام مطلب', db_index=True)
    content = models.TextField(verbose_name='محتوای مطلب')
    average_rating = models.FloatField(default=0.0, blank=True)
    ratings_count = models.PositiveIntegerField(default=0, blank=True)

    def __str__(self):
        return self.title


class Score(BaseModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='مطلب')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=0,
                                     validators=[MinValueValidator(0),
                                                 MaxValueValidator(5),
                                                 ], db_index=True, verbose_name='مقدار امتیاز')

    class Meta:
        unique_together = ('article', 'user')
