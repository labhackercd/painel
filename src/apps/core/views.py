from django.http import JsonResponse
from django.views.generic import TemplateView
from django.db.models import Sum
from apps.core import models
from datetime import date
from dateutil.relativedelta import relativedelta
from collections import defaultdict
import locale


locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['categories'] = models.Category.objects.all()

        category_id = self.request.GET.get('category_id', None)
        show_by = self.request.GET.get('show_by', None)
        offset = int(self.request.GET.get('offset', 0))

        if offset is None or offset < 0:
            offset = 0

        today = date.today()

        if show_by == 'month':
            today = today - relativedelta(months=offset)
            tweets = models.Tweet.objects.filter(created_at__month=today.month)
            previous_month = today - relativedelta(months=1)
            previous_tweets = models.Tweet.objects.filter(
                created_at__month=previous_month.month)
        elif show_by == 'week':
            today = today - relativedelta(weeks=offset)
            end_week = today - relativedelta(days=6)
            tweets = models.Tweet.objects.filter(created_at__lte=today,
                                                 created_at__gte=end_week)
            previous_week = today - relativedelta(weeks=1)
            end_previous_week = previous_week - relativedelta(days=6)
            previous_tweets = models.Tweet.objects.filter(
                created_at__lte=previous_week,
                created_at__gte=end_previous_week)
        else:
            today = today - relativedelta(days=offset)
            tweets = models.Tweet.objects.filter(created_at__contains=today)
            yesterday = today - relativedelta(days=1)
            previous_tweets = models.Tweet.objects.filter(
                created_at__contains=yesterday)

        if category_id:
            tweets = tweets.filter(category_id=category_id)
            previous_tweets = previous_tweets.filter(category_id=category_id)
            context['category'] = models.Category.objects.get(id=category_id)

        current_tweets_count = tweets.count()
        previous_tweets_count = previous_tweets.count()

        try:
            if current_tweets_count == previous_tweets_count:
                variation = 0
            else:
                variation = (
                    current_tweets_count - previous_tweets_count
                ) / previous_tweets_count * 100

            context['variation'] = variation
        except ZeroDivisionError:
            context['variation'] = ''

        profile_ids = list(set(tweets.values_list('profile', flat=True)))
        profiles = models.Profile.objects.filter(id__in=profile_ids)

        context['top_profiles'] = profiles.annotate(
            engagement=Sum('tweets__retweet_count') +
            Sum('tweets__favorite_count'),
            favorite_count=Sum('tweets__favorite_count'),
            retweet_count=Sum('tweets__retweet_count')
        ).order_by('-engagement')[:15]

        context['top_tweets'] = tweets.annotate(
            engagement=Sum('retweet_count') + Sum('favorite_count')
        ).order_by('-engagement')[:15]

        context['profiles_count'] = profiles.count()
        context['tweets_count'] = tweets.count()

        return context


def wordcloud(request):
    today = date.today()
    category_id = request.GET.get('category_id', None)
    show_by = request.GET.get('show_by', None)
    offset = int(request.GET.get('offset', 0))

    if offset is None or offset < 0:
        offset = 0

    if show_by == 'month':
        today = today - relativedelta(months=offset)
        tweets = models.Tweet.objects.filter(created_at__month=today.month)
    elif show_by == 'week':
        today = today - relativedelta(weeks=offset)
        end_week = today - relativedelta(days=6)
        tweets = models.Tweet.objects.filter(created_at__lte=today,
                                             created_at__gte=end_week)
    else:
        today = today - relativedelta(days=offset)
        tweets = models.Tweet.objects.filter(created_at__contains=today)

    if category_id:
        tweets = tweets.filter(category_id=category_id)

    final_dict = {}
    for tweet in tweets:
        most_common = tweet.most_common_stem
        most_common_word = tweet.most_common_word

        if most_common:
            token_data = final_dict.get(most_common, {})
            profiles = token_data.get('profiles', {})
            profile_data = profiles.get(tweet.profile.id, {})

            if profile_data == {}:
                profile_data['image_url'] = tweet.profile.image_url
                profile_data['name'] = tweet.profile.name
                profile_data['screen_name'] = tweet.profile.screen_name
                profile_data['url'] = tweet.profile.url
                profile_data['followers_count'] = tweet.profile.followers_count
                profile_data['verified'] = tweet.profile.verified

            profile_tweets = profile_data.get('tweets', [])

            profile_tweets.append({
                'id': tweet.id_str,
                'text': tweet.text,
                'retweet_count': tweet.retweet_count,
                'favorite_count': tweet.favorite_count,
                'profile': {
                    'image_url': tweet.profile.image_url,
                    'name': tweet.profile.name,
                    'screen_name': tweet.profile.screen_name,
                    'url': tweet.profile.url,
                    'followers_count': tweet.profile.followers_count,
                    'verified': tweet.profile.verified
                }
            })

            profile_data['tweets_count'] = len(profile_tweets)
            profile_data['tweets'] = profile_tweets
            profiles[tweet.profile.id] = profile_data
            token_data['profiles'] = profiles
            token_data['weight'] = len(profiles)
            token_data['name'] = most_common_word

            final_dict[most_common] = token_data

    final_list = [
        {'name': v['name'], 'weight': v['weight'], 'profiles': v['profiles']}
        for k, v in final_dict.items()
    ]

    return JsonResponse(final_list, safe=False)


def areachart(request):
    category_id = request.GET.get('category_id', None)
    show_by = request.GET.get('show_by', None)
    offset = int(request.GET.get('offset', 0))

    if offset is None or offset < 0:
        offset = 0

    if category_id:
        categories = models.Category.objects.filter(id=category_id)
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

        for category in categories:
            for date_result in last_7_results:
                tweet_count = models.Tweet.objects.filter(
                    category=category,
                    created_at__month=date_result.month).count()
                category_data[category.name].append(tweet_count)

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

        for category in categories:
            for i in range(7):
                tweet_count = models.Tweet.objects.filter(
                    category=category,
                    created_at__lte=init_dates[i],
                    created_at__gte=end_dates[i]).count()
                category_data[category.name].append(tweet_count)

    else:
        today = today - relativedelta(days=offset)
        for i in range(7):
            last_7_results.append(today - relativedelta(days=i))

        last_7_results.reverse()

        for category in categories:
            for day in last_7_results:
                tweet_count = models.Tweet.objects.filter(
                    category=category, created_at__contains=day).count()
                category_data[category.name].append(tweet_count)

        last_7_results = [i.strftime('%d %b').upper() for i in last_7_results]

    dataset_result = {
        'labels': last_7_results,
        'categories': category_data
    }

    if today == date.today():
        dataset_result['page_title'] = 'Hoje'
    else:
        dataset_result['page_title'] = last_7_results[-1]

    return JsonResponse(dataset_result, safe=False)
