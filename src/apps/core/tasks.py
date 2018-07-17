from django.conf import settings
from apps.core.models import Profile, Tweet, Category
import tweepy
from painel import celery_app


def process_status(tweet, category_id):
    profile_data = {
        'name': tweet.user.name,
        'screen_name': tweet.user.screen_name,
        'location': tweet.user.location,
        'description': tweet.user.description,
        'url': tweet.user.url,
        'entities': tweet.user.entities,
        'followers_count': tweet.user.followers_count,
        'friends_count': tweet.user.friends_count,
        'listed_count': tweet.user.listed_count,
        'favourites_count': tweet.user.favourites_count,
        'created_at': tweet.user.created_at,
        'lang': tweet.user.lang,
        'image_url': getattr(
            tweet.user, 'profile_image_url_https', None),
        'background_image_url': getattr(
            tweet.user,
            'profile_background_image_url_https', None),
        'banner_url': getattr(
            tweet.user, 'profile_banner_url', None),
    }
    tweet_data = {
        'category_id': category_id,
        'created_at': tweet.created_at,
        'text': tweet.full_text,
        'hashtags': tweet.entities['hashtags'],
        'symbols': tweet.entities['symbols'],
        'user_mentions': tweet.entities['user_mentions'],
        'urls': tweet.entities['urls'],
        'metadata': tweet.metadata,
        'source': tweet.source,
        'geo': tweet.geo,
        'coordinates': tweet.coordinates,
        'place': tweet.place,
        'retweet_count': tweet.retweet_count,
        'favorite_count': tweet.favorite_count,
        'lang': tweet.lang,
    }

    profile = Profile.objects.update_or_create(id_str=tweet.user.id_str,
                                               defaults=profile_data)[0]

    Tweet.objects.update_or_create(id_str=tweet.id_str, profile=profile,
                                   defaults=tweet_data)


@celery_app.task
def collect(categories_id):
    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth, retry_count=3, retry_delay=5,
                     retry_errors=set([401, 404, 500, 503]),
                     wait_on_rate_limit=True)

    categories = Category.objects.filter(id__in=categories_id)

    for category in categories:
        for q in category.queries.all():
            try:
                for tweet in tweepy.Cursor(
                        api.search, q=q.text, tweet_mode='extended',
                        result_type=q.result_type, count=100, lang=q.lang,
                        locale=q.locale, until=q.until, since_id=q.since_id,
                        max_id=q.max_id, geocode=q.geocode).items():
                    process_status(tweet, category.id)
            except tweepy.TweepError as e:
                return e

    return 'Tweets coletados com sucesso!'
