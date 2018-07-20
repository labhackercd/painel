from django.http import JsonResponse
from apps.core import models

# Create your views here.


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

            profile_tweets.append(tweet.id)

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
