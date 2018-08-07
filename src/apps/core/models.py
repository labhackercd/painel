from django.db import models
from django.utils.translation import ugettext_lazy as _


class Profile(models.Model):
    id_str = models.CharField(max_length=200)
    name = models.CharField(max_length=200, null=True, blank=True)
    screen_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    url = models.TextField(null=True, blank=True)
    entities = models.TextField(null=True, blank=True)
    followers_count = models.IntegerField(null=True, blank=True)
    friends_count = models.IntegerField(null=True, blank=True)
    listed_count = models.IntegerField(null=True, blank=True)
    favourites_count = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField()
    lang = models.CharField(max_length=200, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    background_image_url = models.URLField(null=True, blank=True)
    banner_url = models.URLField(null=True, blank=True)
    verified = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        return self.screen_name


class Tweet(models.Model):
    created_at = models.DateTimeField()
    id_str = models.CharField(max_length=200)
    text = models.TextField()
    profile = models.ForeignKey(Profile, related_name='tweets',
                                on_delete=models.CASCADE)
    hashtags = models.TextField(null=True, blank=True)
    symbols = models.TextField(null=True, blank=True)
    user_mentions = models.TextField(null=True, blank=True)
    urls = models.TextField(null=True, blank=True)
    metadata = models.TextField(null=True, blank=True)
    source = models.TextField(null=True, blank=True)
    geo = models.TextField(null=True, blank=True)
    coordinates = models.TextField(null=True, blank=True)
    place = models.TextField(null=True, blank=True)
    retweet_count = models.IntegerField(null=True, blank=True)
    favorite_count = models.IntegerField(null=True, blank=True)
    lang = models.CharField(max_length=200, null=True, blank=True)
    most_common_word = models.CharField(max_length=100, null=True, blank=True)
    most_common_stem = models.CharField(max_length=100, null=True, blank=True)
    is_processed = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('tweet')
        verbose_name_plural = _('tweets')

    def __str__(self):
        return self.text


class Category(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=200)
    description = models.TextField(null=True, blank=True)
    parent = models.ForeignKey("self", null=True, blank=True,
                               on_delete=models.CASCADE,
                               related_name='children')
    tweets = models.ManyToManyField(Tweet, related_name='categories',
                                    blank=True, null=True)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.name


class Query(models.Model):
    RESULT_TYPE_CHOICES = (
        ('popular', _('Popular')),
        ('recent', _('Recent')),
        ('mixed', _('Mixed'))
    )
    text = models.TextField(verbose_name=_("text"))
    result_type = models.CharField(verbose_name=_("result_type"),
                                   max_length=200, choices=RESULT_TYPE_CHOICES,
                                   default='recent')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='queries')
    lang = models.CharField(max_length=200, null=True, blank=True, default='pt')
    locale = models.CharField(max_length=200, null=True, blank=True)
    until = models.CharField(max_length=200, null=True, blank=True,
                             help_text="YYYY-MM-DD")
    since_id = models.CharField(max_length=200, null=True, blank=True)
    max_id = models.CharField(max_length=200, null=True, blank=True)
    geocode = models.CharField(max_length=200, null=True, blank=True,
                               help_text='latitude longitude radius(mi or km)')

    class Meta:
        verbose_name = _('query')
        verbose_name_plural = _('queries')

    def __str__(self):
        return self.category.name
