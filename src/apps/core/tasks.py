from django.conf import settings
from django.utils.timezone import get_current_timezone, make_aware
from apps.core.models import (Profile, Tweet, Category, Mention, Hashtag, Link,
                              Token, TweetCategory)
from lab_text_processing import pre_processing, stopwords, stemmize
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
    TweetCategory.objects.update_or_create(category=category,
                                           tweet=tweet_obj,
                                           defaults={'is_active': False})

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

    return tweet_obj


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
                    tweet_obj = process_status(tweet, category)
                    q.tweets.add(tweet_obj)
            except tweepy.TweepError as e:
                return e
        active_tweet.delay(category.id)

    pre_process.delay()
    collect_link_metatags.delay()
    return 'Tweets coletados com sucesso!'


EXTRA_STOPWORDS = ['pq', 'hj', 'q', 'h', 'vc', 'ta', 'retweeted',
                   'aniversário', 'rolé', 'semestre', 'terça-feira',
                   'quarta-feira', 'segunda-feira', 'quinta-feira',
                   'sexta-feira', 'sextou', 'qdo', 'aovivo', 'número',
                   'daqui', 'artigo', 'sábado', 'domingo', 'sabado', 'inciso',
                   'parágrafo', 'alínea', 'título', 'capítulo', 'seção',
                   'caput', 'subseção', 'felizmente' 'kg', 'oi', 'tb', 'vdd',
                   'olá', 'blá', 'cu', 'ok' 'cê', 'td', 'ñ', 'link', 'oq',
                   'tô', 'dr', 'pau', 'né', 'twitter', 'facebook', 'tbm',
                   'eh', 'liked', 'like', 'porra', 'tipos', 'nao', 'sim', 'n',
                   's', 'nessa', 'mesmo', 'nesta', 'neste', 'coisa', 'cara',
                   'pro', 'to', 'mt', 'já', 'ja', 'caralho', 'kralho',
                   'segunda', 'terça', 'terca', 'quarta', 'quinta', 'sexta',
                   'dps', 'são', 'sao', 'merda', 'x', 'boa', 'foda', 'galera',
                   'rs', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
                   'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
                   'v', 'x', 'w', 'y', 'z', 'kk', 'kkk', 'kkkk', 'kkkkk']


@celery_app.task
def pre_process():
    preprocessor.set_options(
        preprocessor.OPT.URL,
        preprocessor.OPT.EMOJI,
        preprocessor.OPT.NUMBER,
        preprocessor.OPT.RESERVED,
        preprocessor.OPT.MENTION
    )
    stops = stopwords.default_stopwords(
        valid_tags=('adj', 'n', 'prop', 'nprop', 'est', 'npro')
    ) + EXTRA_STOPWORDS
    stops = list(set(stemmize.stemmize(w) for w in stops))
    for tweet in Tweet.objects.filter(is_processed=False):
        cleaned = preprocessor.clean(tweet.text)
        text = re.sub(r'[^\w -]', '', cleaned)
        text = pre_processing.remove_numeric_characters(text)
        stems, ref = pre_processing.clear_tokens(
            pre_processing.tokenize(text), stops
        )
        print(text, stems)

        tweet.is_processed = True
        tweet.save()
        if len(stems) > 0:
            tokens = []
            for stem in stems:
                token = Token.objects.get_or_create(stem=stem)[0]
                token.add_original_word(ref[stem].most_common(1)[0][0])
                token.save()
                tokens.append(token)
            tweet.tokens.set(tokens)
    return 'Tweets pre processados!'


@celery_app.task
def collect_link_metatags():
    for link in Link.objects.filter(collected_metas=False):
        link.collected_metas = True
        try:
            page = requests.get(link.expanded_url, timeout=5)
            tree = fromstring(page.content)
            link.title = tree.xpath("//meta[@property='og:title']/@content")[0]
            link.save()
        except:
            link.save()
            continue

    return 'Links processados com sucesso!'


@celery_app.task
def active_tweet(category_id):
    category = Category.objects.get(id=category_id)
    category_tweets = TweetCategory.objects.filter(category=category)
    category_tweets.update(is_active=False)
    tweets = Tweet.objects.filter(categories=category)
    if category.sql:
        query = str(tweets.query) + " AND " + category.sql
    else:
        query = str(tweets.query)
    tweets_to_active = Tweet.objects.raw(query)
    category_tweets.filter(tweet__in=tweets_to_active).update(is_active=True)

    return 'Tweets da categoria %s ativos.' % category.name


def api_get_objects(url):
    data = requests.get(url).json()
    objects = data['results']

    while(data['next']):
        data = requests.get(data['next']).json()
        objects += data['results']
        print(data['next'])

    return objects


@celery_app.task
def get_babel_profiles():
    url = settings.BABEL_PROFILES_URL
    profiles_data = api_get_objects(url)
    for data in profiles_data:
        profile_data = {}
        profile_data['url'] = data['url']
        profile_data['profile_type_id'] = '1'
        for attr in data['attrs']:
            if attr['field'] == 'profile_image_url':
                profile_data['image_url'] = attr['value']
            else:
                profile_data[attr['field']] = attr['value']
        profile = Profile.objects.update_or_create(id_str=data['id_in_channel'],
                                                   defaults=profile_data)[0]
        print(profile.screen_name)

    return 'Profiles coletados.'
