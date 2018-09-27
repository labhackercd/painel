from django.contrib import admin
from django.contrib import messages
from apps.core.models import (Category, Query, Profile, Tweet, Link, Hashtag,
                              Mention, TweetCategory, ProfileType)
from apps.core.tasks import collect, active_tweet
from django.db.models import Count, F


def start_collect(modeladmin, request, queryset):
    categories_id = queryset.values_list('id', flat=True)
    collect.delay(list(categories_id))
    messages.info(request, "Coleta iniciada")


def activate_tweets_by_sql(modeladmin, request, queryset):
    categories_id = queryset.values_list('id', flat=True)
    for id in categories_id:
        active_tweet.delay(id)
    messages.info(request, "Atualização de tweets iniciada")


def remove_tweets_from_query(modeladmin, request, queryset):
    queries_id = queryset.values_list('id', flat=True)
    for query in queries_id:
        q = Query.objects.get(id=query)
        Tweet.objects.annotate(num_queries=Count('queries')).filter(
            queries__in=[query], num_queries=1).delete()
        for tweet in Tweet.objects.annotate(
            num_queries=Count('queries', distinct=True)).annotate(
                num_categories=Count('categories', distinct=True)).annotate(
                    diference=F('num_queries') - F('num_categories')).filter(
                        queries__in=[query]):
            if (tweet.diference == 0 or
                    tweet.queries.filter(category=q.category).count() == 1):
                TweetCategory.objects.filter(
                    tweet=tweet, category=q.category).delete()
        q.tweets.clear()
    messages.info(request, "Tweets removidos")


start_collect.short_description = "Iniciar coleta"
activate_tweets_by_sql.short_description = "Atualizar estado dos tweets"
remove_tweets_from_query.short_description = "Remover tweets das queries"


class QueryInline(admin.StackedInline):
    model = Query
    exclude = ('tweets',)
    extra = 1


class QueryAdmin(admin.ModelAdmin):
    list_display = ('text', 'category', 'tweets_count')
    search_fields = ('text', 'category__name')
    list_filter = ('category', )
    raw_id_fields = ('tweets',)
    actions = [remove_tweets_from_query]

    def tweets_count(self, obj):
        return obj.tweets.all().count()

    tweets_count.short_description = "tweets count"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'color')
    search_fields = ('name', 'description')
    inlines = (QueryInline, )
    actions = [start_collect, activate_tweets_by_sql]
    raw_id_fields = ('tweets',)


class TweetAdmin(admin.ModelAdmin):
    list_display = ('text', 'profile', 'categories_display')
    search_fields = ('text',)
    list_filter = ('categories', )
    raw_id_fields = ('profile',)

    def categories_display(self, obj):
        return ", ".join([
            category.name for category in obj.categories.all()
        ])

    categories_display.short_description = "Categories"


class TweetCategoryAdmin(admin.ModelAdmin):
    list_display = ('is_active', 'category', 'tweet')
    search_fields = ('tweet__text',)
    list_filter = ('category', 'is_active')
    raw_id_fields = ('tweet', 'category')


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'screen_name', 'verified', 'profile_type')
    search_fields = ('name', 'screen_name')
    list_filter = ('verified', 'profile_type')


class LinkAdmin(admin.ModelAdmin):
    list_display = ('display_url', 'title', 'collected_metas')
    search_fields = ('name', 'screen_name')
    list_filter = ('collected_metas', )
    raw_id_fields = ('tweets',)


class HashtagAdmin(admin.ModelAdmin):
    list_display = ('text',)
    search_fields = ('text',)
    raw_id_fields = ('tweets',)


class MentionAdmin(admin.ModelAdmin):
    list_display = ('id_str', 'name', 'screen_name',)
    search_fields = ('id_str', 'name', 'screen_name')
    raw_id_fields = ('tweets',)


admin.site.register(TweetCategory, TweetCategoryAdmin)
admin.site.register(Query, QueryAdmin)
admin.site.register(ProfileType)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Tweet, TweetAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Hashtag, HashtagAdmin)
admin.site.register(Mention, MentionAdmin)
