from django.contrib import admin

from utilities.admin.mixins import LargeQuerysetMixin, LongIntegerMixin


class CommonModelAdmin(LargeQuerysetMixin, LongIntegerMixin, admin.ModelAdmin):
    pass


class CommonTabularInline(LongIntegerMixin, admin.TabularInline):
    pass


class CommonStackedInline(LongIntegerMixin, admin.StackedInline):
    pass
