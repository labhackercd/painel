from django.http import JsonResponse
from django.views.generic import TemplateView
from django.db.models import Sum, Q, Count
from apps.core import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date
from dateutil.relativedelta import relativedelta
from collections import defaultdict
import locale
import itertools


locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['categories'] = models.Category.objects.all()

        return context


def apply_word_filters(qs, request):
    word = request.GET.get('word', None)
    if word:
        for stem in word.split(','):
            qs = qs.filter(tokens__stem=stem)
    return qs


def areachart(request):
    category_id = request.GET.get('category_id', None)
    show_by = request.GET.get('show_by', None)
    offset = int(request.GET.get('offset', 0))

    if offset is None or offset < 0:
        offset = 0

    if category_id:
        categories = models.Category.objects.filter(id__in=category_id)
    else:
        categories = models.Category.objects.all()

    category_data = defaultdict(dict)
    last_7_results = []

    today = date.today()

    q = get_filter(request)

    if show_by == 'month':
        today = today - relativedelta(months=offset)
        for i in range(7):
            last_7_results.append(today - relativedelta(months=i))

        last_7_results.reverse()

        current_tweets = models.Tweet.objects.filter(
            q,
            created_at__month=last_7_results[-1].month)
        current_tweets = apply_word_filters(current_tweets, request)
        previous_tweets = models.Tweet.objects.filter(
            q,
            created_at__month=last_7_results[-2].month)
        previous_tweets_count = apply_word_filters(
            previous_tweets, request
        ).count()

        for category in categories:
            tweets = category.tweets.filter(
                q,
                created_at__gte=last_7_results[0]
            ).values("created_at").order_by("created_at")
            tweets = apply_word_filters(tweets, request)
            grouped = itertools.groupby(
                tweets, lambda tweet: tweet.get("created_at").strftime("%m"))
            tweets_by_month = {
                int(month): len(list(tweets_this_month))
                for month, tweets_this_month in grouped
            }
            values = [
                tweets_by_month.get(dt.month, 0)
                for dt in last_7_results
            ]
            category_data[category.name] = {'values': values,
                                            'color': category.color}

        last_7_results = [i.strftime('%B').upper() for i in last_7_results]

    elif show_by == 'week':
        today = today - relativedelta(weeks=offset)
        init_dates = []
        end_dates = []
        for i in range(7):
            init_dates.append(today - relativedelta(weeks=i))
            end_dates.append(
                today - relativedelta(
                    weeks=i + 1) + relativedelta(days=1))

        init_dates.reverse()
        end_dates.reverse()

        last_7_results = ['%s - %s' % (
            end_dates[i].strftime('%d %b').upper(),
            init_dates[i].strftime('%d %b').upper()) for i in range(7)]

        current_tweets = models.Tweet.objects.filter(
            q,
            created_at__lte=init_dates[-1],
            created_at__gte=end_dates[-1])
        current_tweets = apply_word_filters(current_tweets, request)
        previous_tweets = models.Tweet.objects.filter(
            q,
            created_at__lte=init_dates[-2],
            created_at__gte=end_dates[-2])
        previous_tweets_count = apply_word_filters(
            previous_tweets, request
        ).count()

        for category in categories:
            values = [
                apply_word_filters(category.tweets.filter(
                    q,
                    created_at__lte=init_dates[i],
                    created_at__gte=end_dates[i]
                ), request).count()
                for i in range(7)
            ]
            category_data[category.name] = {'values': values,
                                            'color': category.color}

    else:
        today = today - relativedelta(days=offset)
        for i in range(7):
            last_7_results.append(today - relativedelta(days=i))

        last_7_results.reverse()

        current_tweets = models.Tweet.objects.filter(
            q,
            created_at__contains=last_7_results[-1])
        current_tweets = apply_word_filters(current_tweets, request)
        previous_tweets = models.Tweet.objects.filter(
            q,
            created_at__contains=last_7_results[-2])
        previous_tweets_count = apply_word_filters(
            previous_tweets, request
        ).count()

        for category in categories:
            tweets = category.tweets.filter(
                q,
                created_at__gte=last_7_results[0]
            ).values("created_at").order_by("created_at")
            tweets = apply_word_filters(tweets, request)
            grouped = itertools.groupby(
                tweets, lambda tweet: tweet.get("created_at").strftime("%d"))
            tweets_by_day = {
                int(day): len(list(tweets_this_day))
                for day, tweets_this_day in grouped
            }
            values = [
                tweets_by_day.get(dt.day, 0)
                for dt in last_7_results
            ]
            category_data[category.name] = {'values': values,
                                            'color': category.color}

        last_7_results = [i.strftime('%d %b').upper() for i in last_7_results]

    dataset_result = {
        'labels': last_7_results,
        'categories': category_data
    }

    if today == date.today() and show_by not in ['week', 'month']:
        dataset_result['page_title'] = 'Hoje'
    else:
        dataset_result['page_title'] = last_7_results[-1]

    current_tweets_count = current_tweets.count()
    profile_ids = list(set(current_tweets.values_list('profile', flat=True)))
    dataset_result['profiles_count'] = len(profile_ids)
    dataset_result['tweets_count'] = current_tweets_count

    try:
        if current_tweets_count == previous_tweets_count:
            dataset_result['variation'] = 0
        else:
            dataset_result['variation'] = (
                current_tweets_count - previous_tweets_count
            ) / previous_tweets_count * 100
    except ZeroDivisionError:
        dataset_result['variation'] = ''

    return JsonResponse(dataset_result, safe=False)


def get_filter(request):
    profile_id = request.GET.get('profile_id', None)
    mentioned_id = request.GET.get('mentioned_id', None)
    hashtag = request.GET.get('hashtag', None)
    link = request.GET.get('link', None)
    category_id = request.GET.get('category_id', None)

    q_filter = Q()

    valid_ids = models.TweetCategory.objects.filter(is_active=True)

    if category_id:
        valid_ids = valid_ids.filter(category__id__in=list(category_id))

    valid_ids = set(valid_ids.values_list('tweet', flat=True))

    q_filter = q_filter & Q(id__in=valid_ids)

    if profile_id:
        q_filter = q_filter & Q(profile_id=profile_id)

    if mentioned_id:
        q_filter = q_filter & Q(mentions__id_str=mentioned_id)

    if hashtag:
        q_filter = q_filter & Q(hashtags__text=hashtag)

    if link:
        q_filter = q_filter & Q(urls__id=link)

    return q_filter


def filter_queryset(manager, request):
    today = date.today()
    word = request.GET.get('word', None)
    category_id = request.GET.get('category_id', None)
    show_by = request.GET.get('show_by', None)
    offset = int(request.GET.get('offset', 0))

    if offset is None or offset < 0:
        offset = 0

    q_filter = Q()

    if category_id:
        q_filter = q_filter & Q(categories__in=list(category_id))

    if show_by == 'month':
        today = today - relativedelta(months=offset)
        q_filter = q_filter & Q(created_at__month=today.month)
    elif show_by == 'week':
        today = today - relativedelta(weeks=offset)
        end_week = today - relativedelta(days=6)
        q_filter = q_filter & Q(created_at__lte=today,
                                created_at__gte=end_week)
    else:
        today = today - relativedelta(days=offset)
        q_filter = q_filter & Q(created_at__contains=today)

    qs = manager.filter(q_filter, get_filter(request))
    if word:
        for stem in word.split(','):
            qs = qs.filter(tokens__stem=stem)

    return qs


def wordcloud(request):
    qs = filter_queryset(models.Tweet.objects.values('tokens__stem'), request)
    words = qs.annotate(weight=Count('tokens__stem')).order_by('-weight')[:20]

    data_result = []
    for word in words:
        if word['tokens__stem']:
            token = models.Token.objects.get(stem=word['tokens__stem'])
            data_result.append({
                'name': token.original,
                'stem': token.stem,
                'weight': word['weight']
            })

    return JsonResponse(data_result, safe=False)


def top_profiles(request):
    top_profiles = filter_queryset(models.Tweet.objects, request).values(
        'profile'
    ).annotate(
        engagement=Sum('retweet_count') + Sum('favorite_count'),
        total_tweets=Count('profile'), total_retweet=Sum('retweet_count'),
        total_favorite=Sum('favorite_count')).order_by('-engagement')[:20]
    data_result = []

    for extra_data in top_profiles:
        profile = models.Profile.objects.get(id=extra_data['profile'])
        data_result.append({
            'id': profile.id,
            'name': profile.name,
            'screen_name': profile.screen_name,
            'image_url': profile.image_url,
            'url': profile.url,
            'verified': profile.verified,
            'followers_count': profile.followers_count,
            'tweets_count': extra_data['total_tweets'],
            'favorite_count': extra_data['total_favorite'],
            'retweet_count': extra_data['total_retweet'],
            'engagement': extra_data['engagement'],
        })

    return JsonResponse(data_result, safe=False)


def tweets(request):
    tweets = filter_queryset(models.Tweet.objects, request).annotate(
        engagement=Sum('retweet_count') + Sum('favorite_count')
    ).order_by('-engagement')

    page = request.GET.get('page', 1)
    paginator = Paginator(tweets, 20)

    try:
        tweets = paginator.page(page)
    except PageNotAnInteger:
        tweets = paginator.page(1)
    except EmptyPage:
        return JsonResponse({'error': 'sem resultados'}, status=400)

    data = [
        {
            'id': tweet.id,
            'tweet_id_str': tweet.id_str,
            'text': tweet.text,
            'retweet_count': tweet.retweet_count,
            'favorite_count': tweet.favorite_count,
            'categories': [c.name for c in tweet.categories.all()],
            'profile': {
                'image_url': tweet.profile.image_url,
                'name': tweet.profile.name,
                'screen_name': tweet.profile.screen_name,
                'url': tweet.profile.url,
                'followers_count': tweet.profile.followers_count,
                'verified': tweet.profile.verified
            }
        }
        for tweet in tweets
    ]

    return JsonResponse(data, safe=False)


def top_links(request):
    top_urls = filter_queryset(models.Tweet.objects, request).exclude(
        urls=None
    ).values(
        'urls__expanded_url', 'urls__title',
        'urls__display_url', 'urls__id'
    ).annotate(
        retweets=Sum('retweet_count') + Count('urls__expanded_url'),
        likes=Sum('favorite_count')
    ).order_by('-retweets', '-likes')[:20]
    data = [
        {'url': link['urls__expanded_url'],
         'id': link['urls__id'],
         'display_url': link['urls__display_url'],
         'title': link['urls__title'],
         'retweets': link['retweets'],
         'likes': link['likes']}
        for link in top_urls
    ]
    return JsonResponse(data, safe=False)


def top_hashtags(request):
    top_tags = filter_queryset(models.Tweet.objects, request).exclude(
        hashtags=None
    ).values(
        'hashtags__text'
    ).annotate(
        retweets=Sum('retweet_count') + Count('hashtags__text')
    ).order_by('-retweets')[:20]
    if top_tags:
        max_retweets = top_tags[0]['retweets']
        data = [
            {'text': tag['hashtags__text'],
             'retweets': tag['retweets'],
             'value': round(tag['retweets'] / max_retweets * 100, 2)}
            for tag in top_tags
        ]
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse([], safe=False)


def top_mentions(request):
    top_mentions = filter_queryset(models.Tweet.objects, request).exclude(
        mentions=None
    ).values(
        'mentions__id_str', 'mentions__screen_name'
    ).annotate(
        retweets=Count('mentions__id_str') + Sum('retweet_count')
    ).order_by('-retweets')[:20]
    data = [
        {'id': mention['mentions__id_str'],
         'screen_name': mention['mentions__screen_name'],
         'retweets': mention['retweets']}
        for mention in top_mentions
    ]

    return JsonResponse(data, safe=False)
