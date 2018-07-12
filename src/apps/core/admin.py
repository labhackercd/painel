from django.contrib import admin
from django.contrib import messages
from apps.core.models import Category, Query, Profile, Tweet
from apps.core.get_tweets import collect


def start_collect(modeladmin, request, queryset):
    msg = collect(queryset)
    messages.info(request, msg)


start_collect.short_description = "Iniciar coleta"


class QueryInline(admin.TabularInline):
    model = Query
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    inlines = (QueryInline, )
    actions = [start_collect]


class TweetAdmin(admin.ModelAdmin):
    list_display = ('text', 'profile', 'category')
    list_filter = ('category', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Profile)
admin.site.register(Tweet, TweetAdmin)
