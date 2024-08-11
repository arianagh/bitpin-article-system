from uuid import uuid4

from django.db import models


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid4, editable=False, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ساخت رکورد')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='زمان به روزرسانی')

    class Meta:
        abstract = True
