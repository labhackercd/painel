from django.conf import settings
from django.db import transaction
from django.utils.timezone import get_current_timezone, make_aware
from apps.core.models import Profile, Tweet, Category, Mention, Hashtag, Link
from lab_text_processing.pre_processing import bow
from lxml.html import fromstring
import preprocessor
import tweepy
import re
import requests

from painel import celery_app


def process_status(tweet, category):
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
        'created_at': make_aware(
            tweet.user.created_at, get_current_timezone(), is_dst=False),
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
        'created_at': make_aware(
            tweet.created_at, get_current_timezone(), is_dst=False),
        'text': tweet.full_text,
        'symbols': tweet.entities['symbols'],
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

    tweet_obj = Tweet.objects.update_or_create(id_str=tweet.id_str,
                                               profile=profile,
                                               defaults=tweet_data)[0]
    category.tweets.add(tweet_obj)

    for user_mention in tweet.entities['user_mentions']:
        mention = Mention.objects.update_or_create(
            id_str=user_mention['id_str'],
            defaults={
                'screen_name': user_mention['screen_name'],
                'name': user_mention['name'],
            }
        )[0]
        mention.tweets.add(tweet_obj)

    for tweet_url in tweet.entities['urls']:
        link = Link.objects.update_or_create(
            expanded_url=tweet_url['expanded_url'],
            defaults={
                'url': tweet_url['url'],
                'display_url': tweet_url['display_url'],
            }
        )[0]
        link.tweets.add(tweet_obj)

    for tweet_hashtag in tweet.entities['hashtags']:
        hashtag = Hashtag.objects.get_or_create(text=tweet_hashtag['text'])[0]
        hashtag.tweets.add(tweet_obj)


@celery_app.task
def collect(categories_id):
    auth = tweepy.OAuthHandler(settings.CONSUMER_KEY, settings.CONSUMER_SECRET)
    auth.set_access_token(settings.ACCESS_TOKEN, settings.ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth, retry_count=3, retry_delay=5,
                     retry_errors=set([401, 404, 500, 503]),
                     wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    categories = Category.objects.filter(id__in=categories_id)

    for category in categories:
        for q in category.queries.all():
            try:
                for tweet in tweepy.Cursor(
                        api.search, q=q.text, tweet_mode='extended',
                        result_type=q.result_type, count=100, lang=q.lang,
                        locale=q.locale, until=q.until, since_id=q.since_id,
                        max_id=q.max_id, geocode=q.geocode).items():
                    process_status(tweet, category)
            except tweepy.TweepError as e:
                return e

    pre_process.delay()
    collect_link_metatags.delay()
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
    for tweet in Tweet.objects.filter(is_processed=False):
        cleaned = preprocessor.clean(tweet.text)
        text = re.sub(r'[^\w -]', '', cleaned)
        tweet_bow, ref = bow(text, extra_stopwords=EXTRA_STOPWORDS)
        tweet.is_processed = True
        if len(tweet_bow) > 0:
            most_common = tweet_bow.most_common(1)[0][0]
            tweet.most_common_stem = most_common
            tweet.most_common_word = ref[most_common].most_common(1)[0][0]
            tweet.save()
    return 'Tweets pre processados!'


@celery_app.task
def collect_link_metatags():
    for link in Link.objects.filter(collected_metas=False):
        link.collected_metas = True
        try:
            page = requests.get(link.expanded_url)
            tree = fromstring(page.content)
            link.title = tree.xpath("//meta[@property='og:title']/@content")[0]
            link.save()
        except IndexError:
            link.save()
            continue

    return 'Links processados com sucesso!'
