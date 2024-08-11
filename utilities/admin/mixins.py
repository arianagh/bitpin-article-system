from django.contrib.admin import widgets
from django.core.paginator import Paginator
from django.db import OperationalError, connection, models, transaction
from django.utils.functional import cached_property


class LongIntegerMixin:
    formfield_overrides = {models.IntegerField: {'widget': widgets.AdminBigIntegerFieldWidget()}, }


class LargeQuerysetPaginator(Paginator):
    @cached_property
    def count(self):
        try:
            with transaction.atomic(), connection.cursor() as cursor:
                cursor.execute('SET LOCAL statement_timeout TO 5;')
                return super().count
        except OperationalError:
            pass

        if not self.object_list.query.where:
            try:
                with transaction.atomic(), connection.cursor() as cursor:
                    cursor.execute("SELECT reltuples FROM pg_class WHERE relname = %s",
                                   [self.object_list.query.model._meta.db_table])
                    estimate = int(cursor.fetchone()[0])
                    return estimate
            except Exception:
                pass
        return super().count


class LargeQuerysetMixin:
    show_full_result_count = False
    paginator = LargeQuerysetPaginator
