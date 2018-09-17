from django.contrib import admin
from django.contrib import messages
from apps.core.models import (Category, Query, Profile, Tweet, Link, Hashtag,
                              Mention, TweetCategory)
from apps.core.tasks import collect, active_tweet


def start_collect(modeladmin, request, queryset):
    categories_id = queryset.values_list('id', flat=True)
    collect.delay(list(categories_id))
    messages.info(request, "Coleta iniciada")


start_collect.short_description = "Iniciar coleta"


def activate_tweets_by_sql(modeladmin, request, queryset):
    categories_id = queryset.values_list('id', flat=True)
    for id in categories_id:
        active_tweet.delay(id)
    messages.info(request, "Atualização de tweets iniciada")


activate_tweets_by_sql.short_description = "Atualizar estado dos tweets"


class QueryInline(admin.StackedInline):
    model = Query
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'color')
    inlines = (QueryInline, )
    actions = [start_collect, activate_tweets_by_sql]
    raw_id_fields = ('tweets',)


class TweetAdmin(admin.ModelAdmin):
    list_display = ('text', 'profile', 'categories_display')
    list_filter = ('categories', )
    raw_id_fields = ('profile',)

    def categories_display(self, obj):
        return ", ".join([
            category.name for category in obj.categories.all()
        ])

    categories_display.short_description = "Categories"


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'screen_name', 'verified')
    list_filter = ('verified', )


class LinkAdmin(admin.ModelAdmin):
    list_display = ('display_url', 'title', 'collected_metas')
    list_filter = ('collected_metas', )
    raw_id_fields = ('tweets',)


class HashtagAdmin(admin.ModelAdmin):
    list_display = ('text', )
    raw_id_fields = ('tweets',)


class MentionAdmin(admin.ModelAdmin):
    list_display = ('screen_name',)
    raw_id_fields = ('tweets',)


admin.site.register(TweetCategory)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tweet, TweetAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Mention, MentionAdmin)
