from django.http import JsonResponse
from django.views.generic import TemplateView
from django.db.models import Sum, Q, Count
from apps.core import models
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

    category_data = defaultdict(list)
    last_7_results = []

    today = date.today()

    if show_by == 'month':
        today = today - relativedelta(months=offset)
        for i in range(7):
            last_7_results.append(today - relativedelta(months=i))

        last_7_results.reverse()

        current_tweets = models.Tweet.objects.filter(
            created_at__month=last_7_results[-1].month)
        previous_tweets_count = models.Tweet.objects.filter(
            created_at__month=last_7_results[-2].month).count()

        for category in categories:
            tweets = category.tweets.filter(
                created_at__gte=last_7_results[0]
            ).values("created_at").order_by("created_at")
            grouped = itertools.groupby(
                tweets, lambda tweet: tweet.get("created_at").strftime("%m"))
            tweets_by_month = {
                int(month): len(list(tweets_this_month))
                for month, tweets_this_month in grouped
            }
            for dt in last_7_results:
                category_data[category.name].append(tweets_by_month.get(dt.month, 0))

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
            created_at__lte=init_dates[-1],
            created_at__gte=end_dates[-1])
        previous_tweets_count = models.Tweet.objects.filter(
            created_at__lte=init_dates[-2],
            created_at__gte=end_dates[-2]).count()

        for category in categories:
            for i in range(7):
                tweet_count = category.tweets.filter(
                    created_at__lte=init_dates[i],
                    created_at__gte=end_dates[i]).count()
                category_data[category.name].append(tweet_count)

    else:
        today = today - relativedelta(days=offset)
        for i in range(7):
            last_7_results.append(today - relativedelta(days=i))

        last_7_results.reverse()

        current_tweets = models.Tweet.objects.filter(
            created_at__contains=last_7_results[-1])
        previous_tweets_count = models.Tweet.objects.filter(
            created_at__contains=last_7_results[-2]).count()

        for category in categories:
            tweets = category.tweets.filter(
                created_at__gte=last_7_results[0]
            ).values("created_at").order_by("created_at")
            grouped = itertools.groupby(
                tweets, lambda tweet: tweet.get("created_at").strftime("%d"))
            tweets_by_day = {
                int(day): len(list(tweets_this_day))
                for day, tweets_this_day in grouped
            }
            for dt in last_7_results:
                category_data[category.name].append(tweets_by_day.get(dt.day, 0))

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
    today = date.today()
    category_id = request.GET.get('category_id', None)
    show_by = request.GET.get('show_by', None)
    offset = int(request.GET.get('offset', 0))

    if offset is None or offset < 0:
        offset = 0

    q_filter = Q()

    if show_by == 'month':
        today = today - relativedelta(months=offset)
        q_filter = Q(created_at__month=today.month)
    elif show_by == 'week':
        today = today - relativedelta(weeks=offset)
        end_week = today - relativedelta(days=6)
        q_filter = Q(created_at__lte=today, created_at__gte=end_week)
    else:
        today = today - relativedelta(days=offset)
        q_filter = Q(created_at__contains=today)

    if category_id:
        q_filter = q_filter & Q(categories__in=list(category_id))

    return q_filter


def wordcloud(request):
    q = get_filter(request)
    words = models.Tweet.objects.filter(q).values('most_common_word').annotate(
        weight=Count('most_common_word')).order_by('-weight')[:20]

    data_result = [
        {'name': word['most_common_word'], 'weight': word['weight']}
        for word in words
    ]

    return JsonResponse(data_result, safe=False)


def top_profiles(request):
    q = get_filter(request)
    tweets = models.Tweet.objects.filter(q).values('id', 'profile')
    tweet_ids = tweets.values_list('id', flat=True)
    profile_ids = list(set(tweets.values_list('profile', flat=True)))
    top_profiles = models.Profile.objects.filter(id__in=profile_ids).annotate(
        engagement=Sum('tweets__retweet_count') +
        Sum('tweets__favorite_count'),
        favorite_count=Sum('tweets__favorite_count'),
        retweet_count=Sum('tweets__retweet_count')
    ).order_by('-engagement')[:15]

    data = []

    for profile in top_profiles:
        profile_tweets = profile.tweets.filter(id__in=tweet_ids)
        tweets_list = []
        for tweet in profile_tweets:
            data_tweet = {
                'id': tweet.id,
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
            tweets_list.append(data_tweet)

        data_profile = {
            'image_url': profile.image_url,
            'name': profile.name,
            'screen_name': profile.screen_name,
            'url': profile.url,
            'followers_count': profile.followers_count,
            'verified': profile.verified,
            'tweets_count': len(tweets_list),
            'favorite_count': profile.favorite_count,
            'retweet_count': profile.retweet_count,
            'tweets': tweets_list
        }
        data.append(data_profile)

    return JsonResponse(data, safe=False)


def top_tweets(request):
    q = get_filter(request)
    top_tweets = models.Tweet.objects.filter(q).annotate(
        engagement=Sum('retweet_count') + Sum('favorite_count')
    ).order_by('-engagement')[:15]
    data = []
    for tweet in top_tweets:
        data_tweet = {
            'id': tweet.id,
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
        data.append(data_tweet)

    return JsonResponse(data, safe=False)
