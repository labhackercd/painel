from django.contrib import admin
from apps.core.models import Category, Query, Profile, Tweet
from apps.core.get_tweets import collect


def start_collect(modeladmin, request, queryset):
    collect(queryset)


start_collect.short_description = "Iniciar coleta"


class QueryInline(admin.TabularInline):
    model = Query
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    inlines = (QueryInline, )
    actions = [start_collect]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Profile)
admin.site.register(Tweet)
