from django.conf import settings
from django.db import transaction
from apps.core.models import Profile, Tweet, Category
from lab_text_processing.pre_processing import bow
import preprocessor
import tweepy
import re

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
        'verified': tweet.user.verified,
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

    tweet = Tweet.objects.update_or_create(id_str=tweet.id_str,
                                           profile=profile,
                                           defaults=tweet_data)[0]


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

    pre_process.delay()
    return 'Tweets coletados com sucesso!'


EXTRA_STOPWORDS = ('pq', 'hj', 'q', 'h', 'vc', 'ta', 'retweeted',
                   'aniversário', 'rolé', 'semestre', 'terça-feira',
                   'quarta-feira', 'segunda-feira', 'quinta-feira',
                   'sexta-feira', 'sextou', 'qdo', 'aovivo', 'número',
                   'daqui', 'artigo', 'sábado', 'domingo', 'sabado', 'inciso',
                   'parágrafo', 'alínea', 'título', 'capítulo', 'seção',
                   'caput', 'subseção', 'felizmente' 'kg', 'oi', 'tb', 'vdd',
                   'olá', 'blá', 'cu', 'ok' 'cê', 'td', 'ñ', 'link', 'oq',
                   'tô', 'dr', 'pau', 'né', 'twitter', 'facebook', 'tbm',
                   'eh', 'liked', 'like', 'porra', 'tipos', 'nao', 'sim', 'n',
                   's')


@celery_app.task
@transaction.atomic
def pre_process():
    preprocessor.set_options(
        preprocessor.OPT.URL,
        preprocessor.OPT.EMOJI,
        preprocessor.OPT.NUMBER,
        preprocessor.OPT.RESERVED,
        preprocessor.OPT.MENTION
    )
    for tweet in Tweet.objects.filter(most_common_stem__isnull=True):
        cleaned = preprocessor.clean(tweet.text)
        text = re.sub(r'[^\w -]', '', cleaned)
        tweet_bow, ref = bow(text, extra_stopwords=EXTRA_STOPWORDS)
        if len(tweet_bow) > 0:
            most_common = tweet_bow.most_common(1)[0][0]
            tweet.most_common_stem = most_common
            tweet.most_common_word = ref[most_common].most_common(1)[0][0]
            tweet.save()
    return 'Tweets pre processados!'
