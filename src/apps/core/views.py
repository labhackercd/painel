from django.http import JsonResponse
from django.views.generic import TemplateView
from django.db.models import Sum
from apps.core import models


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        profiles = models.Profile.objects.all()
        tweets = models.Tweet.objects.all()
        context['top_profiles'] = profiles.annotate(
            engagement=Sum(
                'tweets__retweet_count') + Sum('tweets__favorite_count'),
            favorite_count=Sum('tweets__favorite_count'),
            retweet_count=Sum('tweets__retweet_count')).order_by(
            '-engagement')[:15]
        context['top_tweets'] = tweets.annotate(
            engagement=Sum('retweet_count') + Sum(
                'favorite_count')).order_by(
            '-engagement')[:15]
        context['profiles_count'] = profiles.count()
        context['tweets_count'] = tweets.count()
        context['categories_count'] = models.Category.objects.all().count()

        return context


def wordcloud(request):
    tweets = models.Tweet.objects.all()

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
                    'followers_count': tweet.profile.followers_count
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
        if v['weight'] > 5
    ]

    return JsonResponse(final_list, safe=False)
