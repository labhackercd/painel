from django.contrib import admin
from django.contrib import messages
from apps.core.models import Category, Query, Profile, Tweet
from apps.core.tasks import collect


def start_collect(modeladmin, request, queryset):
    categories_id = queryset.values_list('id', flat=True)
    collect.delay(list(categories_id))
    messages.info(request, "Coleta iniciada")


start_collect.short_description = "Iniciar coleta"


class QueryInline(admin.StackedInline):
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
